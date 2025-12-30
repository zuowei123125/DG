import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QGroupBox, QLabel, QFrame
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import os
class ImportPDFDialog4(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Import Multiple PDF pages')

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 快速换图
        quick_change_group = QGroupBox('版本介绍')
        quick_change_layout = QVBoxLayout(quick_change_group)

        # 创建图像标签1并调整大小
        image_label1 = QLabel()
        # 获取当前脚本所在目录的绝对路径
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # 构建相对路径
        image_filename = "img/微信图片_20230906013631.jpg"
        relative_path = os.path.join(current_directory, image_filename)

        # 创建 QPixmap 对象
        pixmap1 = QtGui.QPixmap(relative_path)
        pixmap1 = pixmap1.scaledToWidth(200)  # 设置宽度限制为200像素
        image_label1.setPixmap(pixmap1)
        quick_change_layout.addWidget(image_label1)

        # 创建文本标签
        text_label1 = QLabel('关注抖音查看视频教程')
        text_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quick_change_layout.addWidget(text_label1)

        # 创建分隔线
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.HLine)
        quick_change_layout.addWidget(divider1)

        # 创建图像标签2并调整大小
        image_label2 = QLabel()
        image_filename2 = "img/微信图片_20230906013548.jpg"
        relative_path2 = os.path.join(current_directory, image_filename2)

        # 创建另一个 QPixmap 对象，使用不同的变量名
        pixmap2 = QtGui.QPixmap(relative_path2)
        pixmap2 = pixmap2.scaledToWidth(200)  # 设置宽度限制为200像素
        image_label2.setPixmap(pixmap2)
        quick_change_layout.addWidget(image_label2)

        # 创建文本标签
        text_label2 = QLabel('BUG提交 功能开发 使用反馈 请联系微信')
        text_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quick_change_layout.addWidget(text_label2)

        # 创建分隔线
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.HLine)
        quick_change_layout.addWidget(divider2)

        # 创建文本标签
        text_label3 = QLabel('PS Mark 版本号1.8(2023.10.4) by:jimi')
        text_label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quick_change_layout.addWidget(text_label3)

        quick_change_group.setLayout(quick_change_layout)
        main_layout.addWidget(quick_change_group)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = ImportPDFDialog4()
    dialog.show()
    sys.exit(app.exec_())
