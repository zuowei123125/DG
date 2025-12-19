import json
import os
#import replicate
import requests
from PyQt5 import QtWidgets, QtGui, QtCore

# from dotenv import load_dotenv
import os

# load_dotenv()  # 加载 .env 文件中的环境变量
url = 'http://43.139.183.222:5000'




class ImportPDFDialog6(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.processed_image_path = None  # 存储处理后的图片路径

    def initUI(self):
        self.setWindowTitle('图像处理参数输入')

        # 布局
        layout = QtWidgets.QVBoxLayout()

        # 文件选择行
        self.file_input = QtWidgets.QLineEdit(self)
      #  self.file_input.setPlaceholderText("选择文件路径 (如 1.jpg)")
        layout.addWidget(self.file_input)

        self.browse_button = QtWidgets.QPushButton('浏览', self)
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        self.prompt_input = QtWidgets.QLineEdit(self)
        self.prompt_input.setPlaceholderText("提示词 ")
        layout.addWidget(self.prompt_input)

        self.creativity_input = QtWidgets.QDoubleSpinBox(self)
        self.creativity_input.setRange(0, 1)
        self.creativity_input.setSingleStep(0.01)
        self.creativity_input.setValue(0.35)  # 默认值
        layout.addWidget(QtWidgets.QLabel("创造力 (0 - 3):"))
        layout.addWidget(self.creativity_input)

        self.resemblance_input = QtWidgets.QDoubleSpinBox(self)
        self.resemblance_input.setRange(0, 3)
        self.resemblance_input.setSingleStep(0.01)
        self.resemblance_input.setValue(0.6)  # 默认值
        layout.addWidget(QtWidgets.QLabel("相似度 (0 - 3):"))
        layout.addWidget(self.resemblance_input)

        self.scale_factor_input = QtWidgets.QSpinBox(self)
        self.scale_factor_input.setRange(2, 8)
        self.scale_factor_input.setValue(2)  # 默认值
        layout.addWidget(QtWidgets.QLabel("放大倍数:"))
        layout.addWidget(self.scale_factor_input)

        self.submit_button = QtWidgets.QPushButton('提交', self)
        self.submit_button.clicked.connect(self.submit)
        layout.addWidget(self.submit_button)

        # 合并图片显示和处理结果区域
        self.output_area = QtWidgets.QVBoxLayout()
        self.image_label = QtWidgets.QLabel(self)
     #   self.image_label.setText("加载的图片将显示在这里")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.output_area.addWidget(self.image_label)

        self.result_display = QtWidgets.QTextEdit(self)
        self.result_display.setReadOnly(True)
        self.output_area.addWidget(QtWidgets.QLabel("处理结果:"))
        self.output_area.addWidget(self.result_display)

        layout.addLayout(self.output_area)

        # 下载按钮
        self.download_button = QtWidgets.QPushButton('下载', self)
        self.download_button.clicked.connect(self.download_image)
        self.download_button.setEnabled(False)  # 初始不可用
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def browse_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择图像文件", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.file_input.setText(file_name)
            self.display_image(file_name)  # 显示选中的图片

    def display_image(self, file_path):
        pixmap = QtGui.QPixmap(file_path)
        self.image_label.setPixmap(pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio))

    def upload_image(self, url, file_path, json_data):
        imgurl = url + "/upload"
        with open(file_path, 'rb') as file:
            files = {'file': file}
            data = {'data': json.dumps(json_data)}  # 将 JSON 数据转换为字符串
            response = requests.post(imgurl, files=files, data=data)

        print(response.status_code)
        response_json = response.json()  # 先解析 JSON 响应

        print(response_json)  # 打印响应内容以检查其格式

        # 确保响应是一个列表，并且至少有一个元素
        if isinstance(response_json, list) and len(response_json) > 0:
            self.processed_image_path = response_json[0]  # 从列表中获取 URL
        else:
            # 处理不符合预期的情况
            print("Unexpected response format:", response_json)
            return

        self.result_display.setPlainText(str(response_json))  # 显示处理结果
        self.download_button.setEnabled(True)  # 启用下载按钮
        self.display_processed_image()  # 显示处理后的图片

    def submit(self):
        try:
            creativity = self.creativity_input.value()
            file_path = self.file_input.text()
            urlprompt = self.prompt_input.text() + " best quality, highres, <lora:more_details:0.5> <lora:SDXLrender_v2.0:1>"
            prompt = urlprompt
            resemblance = self.resemblance_input.value()
            scale_factor = self.scale_factor_input.value()

            if not os.path.exists(file_path):
                raise ValueError("文件不存在，请选择有效的文件。")

            input_data = {
                "seed": 1337,
                "prompt": prompt,
                "dynamic": 6,
                "handfix": "disabled",
                "pattern": False,
                "sharpen": 0,
                "sd_model": "juggernaut_reborn.safetensors [338b85bc4f]",
                "scheduler": "DPM++ 3M SDE Karras",
                "creativity": creativity,
                "lora_links": "",
                "downscaling": False,
                "resemblance": resemblance,
                "scale_factor": scale_factor,
                "tiling_width": 112,
                "tiling_height": 144,
                "output_format": "png",
                "custom_sd_model": "",
                "negative_prompt": "(worst quality, low quality, normal quality:2) JuggernautNegative-neg",
                "num_inference_steps": 18,
                "downscaling_resolution": 768
            }

            # 确保调用时只传递三个参数
            self.upload_image(url, file_path, input_data)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "错误", str(e))


    def run(url):

        newurl = url + "/data"
        data = {'key': 'value'}  # 你要发送的数据
        response = requests.post(newurl, json=data)

        print(response.status_code)  # 打印状态码
        print(response.json())  # 打印返回的 JSON 数据

    def run2(url):

        newurl = url + "/dataimg"
        data = {'key': 'value'}  # 你要发送的数据
        response = requests.post(newurl, json=data)

        print(response.status_code)  # 打印状态码
        print(response.json())  # 打印返回的 JSON 数据


    # if __name__ == '__main__':
    #     upload_image(url, '1.jpg', {'key': 'value'})



    def display_processed_image(self):
        # 下载并显示处理后的图片
        response = requests.get(self.processed_image_path)
        if response.status_code == 200:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(response.content)
            self.image_label.setPixmap(pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio))

    def download_image(self):
        if self.processed_image_path:
            image_url = self.processed_image_path

            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "保存处理后的图片", "", "Image Files (*.png *.jpg *.jpeg)")
            if file_name:
                try:
                    response = requests.get(image_url)
                    response.raise_for_status()  # 检查请求是否成功
                    with open(file_name, 'wb') as f:
                        f.write(response.content)
                    QtWidgets.QMessageBox.information(self, "成功", "图片下载完成！")
                except requests.exceptions.RequestException as e:
                    QtWidgets.QMessageBox.critical(self, "错误", f"下载失败：{e}")
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "错误", f"文件保存失败：{e}")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    # 创建并显示登录界面
    # login_dialog = LoginDialog()
    # if login_dialog.exec_() == QtWidgets.QDialog.Accepted:
        # 只有在登录成功后才执行以下代码
    ex = ImportPDFDialog6()
    ex.show()

    sys.exit(app.exec_())