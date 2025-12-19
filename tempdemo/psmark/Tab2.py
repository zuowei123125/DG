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


class YourMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RUNDXF")

        layout = QVBoxLayout()

        self.button1 = QPushButton("DXF文件路径")
        self.button1.setFixedWidth(200)
        self.button1.clicked.connect(self.showDxfFileDialog)

        self.button2 = QPushButton("PLT文件路径")
        self.button2.setFixedWidth(200)
        self.button2.clicked.connect(self.showPltFileDialog)

        self.initial_button1_text = self.button1.text()
        self.initial_button2_text = self.button2.text()

        panel1 = QGroupBox("文件路径")
        panel1_layout = QVBoxLayout(panel1)
        panel1_layout.setSpacing(10)
        panel1_layout.setContentsMargins(10, 10, 10, 10)
        panel1_layout.addWidget(self.button1)
        panel1_layout.addWidget(self.button2)
        layout.addWidget(panel1)

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

        self.clearButton = QPushButton("清空信息")
        self.clearButton.clicked.connect(self.clearScrollArea)
        layout.addWidget(self.clearButton)

        confirm_button = QPushButton("分割")
        confirm_button.clicked.connect(self.updateScrollArea)
        #confirm_button.clicked.connect(self.freezeAndParse)  # 连接按钮点击事件
        layout.addWidget(confirm_button)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.dxfLineEdits = {}

        self.allowButtonActions = True  # 标志变量，控制是否允许按钮行为





    def run_coreldraw_macros(self):
        try:
            dogms = win32com.client.DispatchEx("CorelDRAW.Application.23")

            macros_to_run = [
                "RUN.OpenDXFFilesInFolder",
                "RUN.RotateSelectionClockwise",
                "RUN.DeleteUnnamedSublayers",
                "RUN.StToFront",
                "RUN.IterateSublayerNames",


            ]

            for macro in macros_to_run:
                dogms.GMSManager.RunMacro("RUNDXF", macro)


        except Exception as e:
            QMessageBox.warning(self, "警告", "缺少CDR模块，请载入CDR模块", QMessageBox.Ok)
        #    print("缺少CDR模块，请载入CDR模块")






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
            self.initial_dxf_path = file_path  # 更新初始路径而不更新按钮文本
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

    def process_dxf_file(self, file_path, extracted_content):
        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()
        mspBox = ezdxf.bbox.extents(msp)

        print("=====", os.path.basename(file_path))
        print("左上角坐标:", mspBox.extmin)
        print("画布宽:", mspBox.size[0], "画布高:", mspBox.size[1])
        print()

        for entity in msp.query():
            if entity.dxftype() == "INSERT":
                temp = []
                rotation = None
                block = doc.blocks[entity.dxf.name]

                for e in block:
                    if e.dxftype() != "TEXT":
                        temp.append(e)
                    else:
                        rotation = e.dxf.rotation

                if rotation is not None:
                    rotation %= 360
                    if 45 <= rotation < 135:
                        rotation = 90
                    elif 135 <= rotation < 225:
                        rotation = 180
                    elif 225 <= rotation < 315:
                        rotation = -90
                    else:
                        rotation = 0

                    print("=====", entity.dxf.name)
                    print("大小:", ezdxf.bbox.extents(temp).size)
                    print("文字角度:", rotation)

                    center = ezdxf.bbox.extents(temp).center
                    center = (center.x, mspBox.extmax.y - center.y)  # 调整center y值

                    print("中心坐标:", center)

                    center = (center[1], mspBox.size[0] - center[0])  # 旋转后中心坐标
                    print("旋转后中心坐标:", center)

                    separator = "_"  # 分隔符
                    entity.dxf.name += separator + str(rotation)
                    block.name += separator + str(rotation)

        new_file_path = os.path.join(r"D:\marktemp", "{}.dxf".format(extracted_content))
        doc.saveas(new_file_path)
    def getSinglePieceCount(self):
        return self.lineEdit3.text()

    def recreate_folders(self):
        # 定义文件夹路径
        folder_paths = [r"D:\PSMARKtemp", r"D:\marktemp"]

        # 删除文件夹及其内容
        for folder_path in folder_paths:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder_path}")

        # 重新创建文件夹
        for folder_path in folder_paths:
            os.makedirs(folder_path)
            print(f"Recreated folder: {folder_path}")

    def freezeAndParse(self):
        self.parse_button.setEnabled(False)  # 冻结按钮
        QTimer.singleShot(10000, self.unfreezeButton)  # 10秒后解冻按钮

    def unfreezeButton(self):
        self.parse_button.setEnabled(True)  # 解冻按钮


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






        corel_app = win32com.client.Dispatch("CorelDRAW.Application.23")

        # 获取当前活动文档
        active_document = corel_app.ActiveDocument

        # 获取当前页面中所有图层的名称，排除特定名称的图层
        layer_names = [layer.Name for layer in active_document.ActivePage.Layers
                       if layer.Name not in ["辅助线", "1", "0", "Defpoints"]]

        p_numbers = []  # 初始化存储 P 数字的列表

        for code, quantity in code_quantities.items():
            for i in range(1, single_code_pieces + 1):
                p_numbers.extend([f"P{i}"] * int(quantity))

        print(p_numbers)


        # 循环遍历不同的码
        # p_numbers = []  # 初始化存储 P 数字的列表
        #
        # for code, quantity in code_quantities.items():
        #     for i in range(1, single_code_pieces + 1):
        #         # 根据码的数量分别生成对应数量的 P 数字，并添加到列表中
        #         p_numbers.extend([f"P{i}"] * quantity)
        #         print(p_numbers)
        new_layer_names = []
        index = 0
        for old_name in layer_names:
            parts = old_name.split("-")  # 根据"-"分割字符串
            if len(parts) > 1:
                new_name = f"{p_numbers[index]}-{parts[1]}"  # 使用数组中的 P 数字
                new_layer_names.append(new_name)
                index += 1

        # 在新的图层名数组中遍历，对图层进行修改
        modified_names = []  # 创建一个列表来存储修改后的名称
        modified_names2 = []
        for i, new_name in enumerate(new_layer_names):
            active_document.ActivePage.Layers(layer_names[i]).Name = new_name
            modified_names2.append(new_name)
            modified_names.append(new_name)
            print(f"Modified: {layer_names[i]} -> {new_name}")



      #  print(modified_names)


        def delete_layers_by_names(names_to_delete, active_document):
            corel_app = win32com.client.Dispatch("CorelDRAW.Application.23")

            # 获取当前活动文档
            active_document = corel_app.ActiveDocument
            for target_layer_name in names_to_delete:
                for layer in active_document.ActivePage.Layers:
                    if layer.Name == target_layer_name:
                        layer.Delete()
                        break  # 找到目标图层后中断循环



        modified_names_list = []  # 用于存储每次循环中的 modified_names 列表

        Index = 0
        for code in code_quantities:
            quantity = code_quantities[code]
            total_pieces = quantity * single_code_pieces

            # 获取数组的前 total_pieces 个元素
            newmodified_names_filtered = modified_names[:total_pieces]
         #   print(newmodified_names_filtered)

            result_array = [fruit for fruit in modified_names2 if fruit not in newmodified_names_filtered]
            result_array_length = len(result_array)
            print(result_array_length)

            delete_layers_by_names(result_array, active_document.ActivePage)
          #  modified_names_list.append(modified_names)  # 将 modified_names 添加到数组中


            dogms = win32com.client.DispatchEx("CorelDRAW.Application.23")

            dogms.GMSManager.RunMacro("RUNDXF", "RUN.ExportSelectionToPSD", Index)

            dogms.GMSManager.RunMacro("RUNDXF", "RUN.HOURUN", result_array_length)

            modified_names = modified_names[total_pieces:]

            Index += 1


        corel_app = win32com.client.Dispatch("CorelDRAW.Application.23")

        corel_app .GMSManager.RunMacro("RUNDXF", "RUN.ActiveDocumentClose")

        QMessageBox.warning(self, "提醒", "分割完成，请进行裁片套版操作。")

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
    mainWindow = YourMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())