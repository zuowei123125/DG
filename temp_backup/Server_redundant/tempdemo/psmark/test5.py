import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, \
    QLineEdit, QScrollArea, QGroupBox, QHBoxLayout, QMessageBox, QProgressDialog
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QTimer
import re
import os
import ezdxf
import ezdxf.tools
import ezdxf.bbox
import ezdxf.units
import ezdxf.math
from coreldraw_checker import is_coreldraw_running
from functools import partial
import win32com.client
import os
import shutil
import threading
from clear_folder import another_function


class YourMainWindow9(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RUNDXF")

        layout = QVBoxLayout()

        self.button2 = QPushButton("裁片文件路径")
        self.button2.setFixedWidth(200)
        self.button2.clicked.connect(self.showPltFileDialog)

        self.button1 = QPushButton("DXF文件路径")
        self.button1.setFixedWidth(200)
        self.button1.clicked.connect(self.showDxfFileDialog)

        self.initial_button2_text = self.button2.text()

        self.initial_button1_text = self.button1.text()

        panel1 = QGroupBox("文件路径")
        panel1_layout = QVBoxLayout(panel1)
        panel1_layout.setSpacing(10)
        panel1_layout.setContentsMargins(10, 10, 10, 10)
        panel1_layout.addWidget(self.button2)
        panel1_layout.addWidget(self.button1)

        layout.addWidget(panel1)

        self.label7 = QLabel('文档名称')
        self.lineEdit7 = QLineEdit()
        self.lineEdit7.setValidator(QIntValidator())
        self.lineEdit7.setFixedSize(120, 30)
        layout.addWidget(self.label7)
        layout.addWidget(self.lineEdit7)

        self.label6 = QLabel('分辨率大小')
        self.lineEdit6 = QLineEdit()
        self.lineEdit6.setValidator(QIntValidator())
        self.lineEdit6.setFixedSize(120, 30)
        layout.addWidget(self.label6)
        layout.addWidget(self.lineEdit6)





        self.label5 = QLabel('单码片数')
        self.lineEdit3 = QLineEdit()
        self.lineEdit3.setValidator(QIntValidator())
        self.lineEdit3.setFixedSize(120, 30)
        layout.addWidget(self.label5)
        layout.addWidget(self.lineEdit3)


        self.scrollWidget = QWidget()
        self.scrollWidgetLayout = QVBoxLayout(self.scrollWidget)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)
        layout.addWidget(self.scrollArea)
        #
        # self.clearButton = QPushButton("清空信息")
        # self.clearButton.clicked.connect(self.clearScrollArea)
        # layout.addWidget(self.clearButton)

        # self.bigconfirm_button = QPushButton("混码分割")
        # self.bigconfirm_button.clicked.connect(self.bigupdateScrollArea)
        # layout.addWidget(self.bigconfirm_button)

        confirm_button = QPushButton("运行")
        confirm_button.clicked.connect(self.updateScrollArea)
        layout.addWidget(confirm_button)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.dxfLineEdits = {}

        self.allowButtonActions = True  # 标志变量，控制是否允许按钮行为









    def showPltFileDialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择PLT文件", "", "PLT Files (*.plt);;All Files (*)",
                                                   options=options)
        if file_path:
            print("Selected PLT file:", file_path)
            extracted_content = self.extract_content_from_plt_path(file_path)
            print(extracted_content)
            self.sizes = self.fill_sizes_from_extracted_content(extracted_content)

            # 更新尺寸字典后，清空并填充滚动区域
            self.clearScrollArea()
            self.populateScrollArea()

            self.initial_plt_path = file_path  # 更新初始路径而不更新按钮文本

        else:
            print("No PLT file selected")
            QMessageBox.warning(self, "警告", "没有选择文件夹。请重新选择文件夹。", QMessageBox.Ok)

            pass

    def showDxfFileDialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择DXF文件", "", "DXF Files (*.dxf);;All Files (*)",
                                                   options=options)
        if file_path:
            print("Selected DXF file:", file_path)
            extracted_content = self.extract_content_from_plt_path(file_path)  # 更新初始路径而不更新按钮文本
            print(extracted_content)
            self.sizes = self.fill_sizes_from_extracted_content(extracted_content)

            # 更新尺寸字典后，清空并填充滚动区域
            self.clearScrollArea()
            self.populateScrollArea()

            self.initial_plt_path = file_path  # 更新初始路径而不更新按钮文本
        else:
            print("No DXF file selected")
            QMessageBox.warning(self, "警告", "没有选择文件夹。请重新选择文件夹。", QMessageBox.Ok)
            # 在此处添加提醒逻辑，例如使用 QMessageBox 提示用户没有选择文件

    def extract_content_from_plt_path(self, plt_path):
        match = re.search(r'\((.*?)\)', plt_path)
        if match:
            extracted_content = match.group(1)
            return extracted_content
        else:
            return "No content in parentheses found"

    def fill_sizes_from_extracted_content(self, extracted_content):
        sizes = extracted_content.split("+")
        size_dict = {}
        for size in sizes:
            size_dict[size] = ""
        return size_dict




    def updateScrollArea(self):

        another_function()

        if not is_coreldraw_running():
            QMessageBox.warning(self, "警告", "CorelDRAW未运行，无法执行操作。")
            return

        plt_file_path = self.initial_plt_path

        # 获取DXF文件路径
        dxf_file_path = self.initial_dxf_path
        extracted_content = self.extract_content_from_plt_path(plt_file_path)

        if dxf_file_path:
            # 去掉括号内内容后的PLT文件名作为DXF文件名
            plt_filename = os.path.basename(plt_file_path)
       #     dxf_filename = re.sub(r'\(.*?\)', '', plt_filename)
            self.process_dxf_file(dxf_file_path, extracted_content)  # 调用解析函数并传入单码片数和新的DXF文件名
            print("DXF文件解析完成！")
        else:
            QMessageBox.warning(self, "警告", "没有选择DXF文件。请先选择一个DXF文件。", QMessageBox.Ok)
            print()



        self.run_coreldraw_macros()
        single_code_pieces = int(self.getSinglePieceCount()) # 获取单码片数
        print(single_code_pieces)
        # 打印滚动区域中的输入框内容
        code_quantities = {}  # 创建一个新的字典用于存储数据

        for label, line_edit in self.dxfLineEdits.items():
            text = line_edit.text()
            if text.isdigit():
                value = int(text)  # 尝试将文本转换为整数
            else:
                try:
                    value = float(text)  # 尝试将文本转换为浮点数
                except ValueError:
                    print(f"Invalid value for {label}: {text}")
                    continue  # 转换失败，跳过当前循环迭代

            code_quantities[label] = value  # 存储转换后的数字到字典

        print(code_quantities)
        length = len(code_quantities)
        print(length)  # 输出 3，因为字典中有三对键值对






    def updateLineEditsFromSizes(self):
            for size_label, line_edit in self.dxfLineEdits.items():
                self.sizes[size_label] = line_edit.text()

    def populateScrollArea(self):
        self.clearScrollArea()
        for size_label, size_text in self.sizes.items():
            size_layout = QHBoxLayout()
            size_layout.addWidget(QLabel(size_label))

            line_edit = QLineEdit()
            line_edit.setValidator(QIntValidator())
            line_edit.setFixedSize(100, 30)
            line_edit.setText(size_text)

            self.dxfLineEdits[size_label] = line_edit
            size_layout.addWidget(line_edit)

            self.scrollWidgetLayout.addLayout(size_layout)

    def clearScrollArea(self):
        for i in reversed(range(self.scrollWidgetLayout.count())):
            item = self.scrollWidgetLayout.itemAt(i)
            if isinstance(item, QHBoxLayout) or isinstance(item, QVBoxLayout):
                while item.count():
                    widget = item.takeAt(0).widget()
                    if widget:
                        widget.deleteLater()
        self.dxfLineEdits.clear()  # 清空部件引用




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = YourMainWindow9()
    mainWindow.show()
    sys.exit(app.exec_())