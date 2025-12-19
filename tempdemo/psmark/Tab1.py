
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSpinBox, QFormLayout, QTabWidget, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QGroupBox, QLineEdit, QCheckBox, QMessageBox
from PyQt5.QtGui import QIcon
import piece_decorative
import re
from PyQt5.QtWidgets import QApplication


class ImportPDFDialog(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Import Multiple PDF pages')
        self.setWindowIcon(QIcon('icon.png'))

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        psd_group = QGroupBox('PSD裁片预处理')
        psd_layout = QVBoxLayout(psd_group)
        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(0)
        self.spin_box.setMaximum(100)
        self.spin_box.setValue(1)
        psd_layout.addWidget(self.spin_box)
        self.number_button = QPushButton('名称赋予')
        self.number_button.clicked.connect(self.number_button_clicked)
        psd_layout.addWidget(self.number_button)
        form_layout = QFormLayout()
        # fabric_break_button = QPushButton('设置裁片组')
        # fabric_break_button.clicked.connect(self.break_fabric_line)
        # psd_layout.addWidget(fabric_break_button)

        # self.shrink_width_line_edit = QLineEdit()
        # form_layout.addRow('缩水值宽:', self.shrink_width_line_edit)
        # self.shrink_height_line_edit = QLineEdit()
        # form_layout.addRow('缩水值高:', self.shrink_height_line_edit)
        #
        # psd_layout.addLayout(form_layout)
        # psd_pattern_button = QPushButton('缩水修改')
        # psd_pattern_button.clicked.connect(self.set_psd_pattern)
        # psd_layout.addWidget(psd_pattern_button)
        psd_place_button = QPushButton('角度校准')
        psd_place_button.clicked.connect(self.place_psd_pieces)
        psd_layout.addWidget(psd_place_button)
        psdcut_grab_button = QPushButton('花样裁切')
        psdcut_grab_button.clicked.connect(self.psdcut)
        psd_layout.addWidget(psdcut_grab_button)
        psd_grab_button = QPushButton('裁片抓取')
        psd_grab_button.clicked.connect(self.grab_psd_pieces)
        psd_layout.addWidget(psd_grab_button)

        main_layout.addWidget(psd_group)

        psd_group2 = QGroupBox('缩水修改')
        psd_layout = QVBoxLayout(psd_group2)
        # self.spin_box = QSpinBox()
        # self.spin_box.setMinimum(0)
        # self.spin_box.setMaximum(100)
        # self.spin_box.setValue(1)
        # psd_layout.addWidget(self.spin_box)
        # self.number_button = QPushButton('名称赋予')
        # self.number_button.clicked.connect(self.number_button_clicked)
        # psd_layout.addWidget(self.number_button)
        # form_layout = QFormLayout()
        # fabric_break_button = QPushButton('设置裁片组')
        # fabric_break_button.clicked.connect(self.break_fabric_line)
        # psd_layout.addWidget(fabric_break_button)

        self.shrink_width_line_edit = QLineEdit()
        form_layout.addRow('缩水值宽:', self.shrink_width_line_edit)
        self.shrink_height_line_edit = QLineEdit()
        form_layout.addRow('缩水值高:', self.shrink_height_line_edit)

        psd_layout.addLayout(form_layout)
        psd_pattern_button = QPushButton('缩水修改')
        psd_pattern_button.clicked.connect(self.set_psd_pattern)
        psd_layout.addWidget(psd_pattern_button)
        # psd_place_button = QPushButton('角度校准')
        # psd_place_button.clicked.connect(self.place_psd_pieces)
        # psd_layout.addWidget(psd_place_button)
        # psdcut_grab_button = QPushButton('花样裁切')
        # psdcut_grab_button.clicked.connect(self.psdcut)
        # psd_layout.addWidget(psdcut_grab_button)
        # psd_grab_button = QPushButton('裁片抓取')
        # psd_grab_button.clicked.connect(self.grab_psd_pieces)
        # psd_layout.addWidget(psd_grab_button)

        main_layout.addWidget(psd_group2)




        # 添加六个按钮，每行三个按钮
        align_group = QGroupBox('裁片对齐')
        align_layout = QVBoxLayout(align_group)

        # 创建水平布局用于放置每行的按钮
        row_layout = QHBoxLayout()

        # 创建第一个按钮
        neckline_align_button = QPushButton('左上对齐')
        neckline_align_button.clicked.connect(self.align_neckline1)
        row_layout.addWidget(neckline_align_button)

        # 创建第二个按钮
        button2 = QPushButton('领口对齐')
        button2.clicked.connect(self.another_function2)
        row_layout.addWidget(button2)

        # 创建第三个按钮
        button3 = QPushButton('右上对齐')
        button3.clicked.connect(self.another_function3)
        row_layout.addWidget(button3)

        # 将第一行按钮添加到垂直布局
        align_layout.addLayout(row_layout)

        # 创建水平布局用于放置第二行的按钮
        row_layout = QHBoxLayout()

        # 创建第四个按钮
        button4 = QPushButton('左下对齐')
        button4.clicked.connect(self.another_function4)
        row_layout.addWidget(button4)

        # 创建第五个按钮
        button5 = QPushButton('下摆对齐')
        button5.clicked.connect(self.another_function5)
        row_layout.addWidget(button5)

        # 创建第六个按钮
        button6 = QPushButton('右下对齐')
        button6.clicked.connect(self.another_function6)
        row_layout.addWidget(button6)

        # 将第二行按钮添加到垂直布局
        align_layout.addLayout(row_layout)

        main_layout.addWidget(align_group)

        main_layout.addWidget(align_group)
        info_group = QGroupBox('信息写入')
        info_layout = QVBoxLayout(info_group)
        size_add_button = QPushButton('添加定位点')
        size_add_button.clicked.connect(self.add_sizes)
        info_layout.addWidget(size_add_button)
        # material_count_button = QPushButton('缩放信息写入')
        # material_count_button.clicked.connect(self.count_materials)
        # info_layout.addWidget(material_count_button)

        material_count_button2 = QPushButton('重写缩放信息')
        material_count_button2.clicked.connect(self.count_materials2)
        info_layout.addWidget(material_count_button2)



        main_layout.addWidget(info_group)
        pattern_group = QGroupBox('自动套花')
        pattern_layout = QVBoxLayout(pattern_group)
        pattern_extend_button = QPushButton('通码延申')
        pattern_extend_button.clicked.connect(self.extend_pattern)
        pattern_layout.addWidget(pattern_extend_button)
        scale_button = QPushButton('宽高缩放')
        scale_button.clicked.connect(self.scale_dimensions)
        pattern_layout.addWidget(scale_button)
        proportional_scale_button = QPushButton('比例缩放')
        proportional_scale_button.clicked.connect(self.proportional_scale)
        pattern_layout.addWidget(proportional_scale_button)

        bigproportional_scale_button = QPushButton('定位点比例缩放')
        bigproportional_scale_button.clicked.connect(self.bigproportional_scale)
        pattern_layout.addWidget(bigproportional_scale_button)

        # self.checkbox1 = QCheckBox('混排套图方法', self)
        # pattern_layout.addWidget(self.checkbox1)

        main_layout.addWidget(pattern_group)
        save_group = QGroupBox('文档保存')
        save_layout = QVBoxLayout(save_group)
        # add_size_button = QPushButton('尺码激活')
        # add_size_button.clicked.connect(self.add_size_to_layers)
        # save_layout.addWidget(add_size_button)
        form_layout = QFormLayout()
        self.prefix_line_edit = QLineEdit()
        form_layout.addRow('前缀添加:', self.prefix_line_edit)
        save_layout.addLayout(form_layout)
        save_button = QPushButton('保存')
        save_button.clicked.connect(self.save_document2)
        save_layout.addWidget(save_button)
        main_layout.addWidget(save_group)


    def align_neckline1(self):

        piece_decorative.PS_DXF7_jscode_fun('左上对齐2()')
        pass

    def another_function2(self):

        piece_decorative.PS_DXF3_jscode_fun('领口对齐2()')
        pass

    def another_function3(self):
        piece_decorative.PS_DXF2_jscode_fun('右上对齐2()')
        # piece_decorative.PS_DXF2_jscode_fun(f'文档保存最新("{前缀}");')
        pass


    def another_function4(self):
        piece_decorative.PS_DXF4_jscode_fun('左下对齐2()')
        # piece_decorative.PS_DXF2_jscode_fun(f'文档保存最新("{前缀}");')
        pass

    def another_function5(self):
        piece_decorative.PS_DXF5_jscode_fun('下摆对齐2()')
        # piece_decorative.PS_DXF2_jscode_fun(f'文档保存最新("{前缀}");')
        pass

    def another_function6(self):
        piece_decorative.PS_DXF6_jscode_fun('右下对齐2()')
        # piece_decorative.PS_DXF2_jscode_fun(f'文档保存最新("{前缀}");')
        pass

    def save_document2(self):
        前缀 = self.prefix_line_edit.text()
        piece_decorative.PS_DXF2_jscode_fun(f'文档保存最新("{前缀}");')


    def add_size_to_layers(self):
        piece_decorative.PS_DXF2_jscode_fun('信息激活2();')


    def psdcut(self):
        piece_decorative.PS_DXF6_jscode_fun('图像切割2();')

    def number_button_clicked(self):
        current_value = self.spin_box.value()
        piece_decorative.PS_DXF_jscode_fun(f"名称赋予({current_value});")
        new_value = current_value + 1
        self.spin_box.setValue(new_value)

    def another_function(self):
        # 在这里定义按钮点击事件的处理逻辑
        pass
    def set_psd_pattern(self):
        高度值 = self.shrink_height_line_edit.text()
        宽度值 = self.shrink_width_line_edit.text()

        number_pattern = re.compile(r'^\d+(\.\d+)?$')  # 正则表达式匹配数字格式

        if number_pattern.match(高度值) and number_pattern.match(宽度值):
            # 如果两个值都是数字，执行批量缩水操作
          #  piece_decorative.PS_DXF2_jscode_fun('设置花样组删除图层设置名称();')
            piece_decorative.PS_DXF2_jscode_fun(f"批量缩水值修改({宽度值},{高度值});")
        else:
            # 如果至少有一个值不是数字，显示警告
            QMessageBox.warning(self, '错误', '缩水值只能是数字！')

    def grab_psd_pieces(self):
        piece_decorative.PS_DXF2_jscode_fun('设置花样组删除图层设置名称();')
        piece_decorative.PS_DXF12_jscode_fun('批量套数写入();')
        piece_decorative.PS_DXF2_jscode_fun('设置花样组2();')
        piece_decorative.PS_DXF_jscode_fun('裁片吸取2();')
        piece_decorative.PS_DXF2_jscode_fun('设置花样组顺序居中();')
        piece_decorative.PS_DXF_jscode_fun('信息写入();')
        piece_decorative.PS_DXF3_jscode_fun('裁片视图检查2();')

    def place_psd_pieces(self):
        piece_decorative.PS_DXF3_jscode_fun('角度旋转();')

    def align_neckline(self):
        piece_decorative.PS_DXF2_jscode_fun('领口对齐();')


    def extend_pattern(self):

        # if self.checkbox1.isChecked():
        #     piece_decorative.PS_DXF_jscode_fun('删除指定名称蒙版();')
        #     piece_decorative.PS_DXF20_jscode_fun('混排通码延申导出();')
        #     print('按下')
        #
        # else:
        #     print('没有按下')
            piece_decorative.PS_DXF6_jscode_fun('前景色修改();')
            piece_decorative.PS_DXF_jscode_fun('删除指定名称蒙版();')
            piece_decorative.PS_DXF_jscode_fun('裁片射出();')
            piece_decorative.PS_DXF2_jscode_fun('信息激活2();')

    def scale_dimensions(self):
        piece_decorative.PS_DXF6_jscode_fun('前景色修改();')
        piece_decorative.PS_DXF_jscode_fun('删除指定名称蒙版();')
        piece_decorative.PS_DXF3_jscode_fun('裁片射出宽高缩放();')
        piece_decorative.PS_DXF2_jscode_fun('信息激活2();')

    def proportional_scale(self):
        piece_decorative.PS_DXF6_jscode_fun('前景色修改();')
        piece_decorative.PS_DXF_jscode_fun('删除指定名称蒙版();')
        piece_decorative.PS_DXF9_jscode_fun('裁片射出比例缩放按中心点();')
        piece_decorative.PS_DXF2_jscode_fun('信息激活2();')

    def bigproportional_scale(self):
        piece_decorative.PS_DXF6_jscode_fun('前景色修改();')
        piece_decorative.PS_DXF_jscode_fun('删除指定名称蒙版();')
        piece_decorative.PS_DXF11_jscode_fun('裁片射出缩放();')
        piece_decorative.PS_DXF2_jscode_fun('信息激活2();')



    def add_sizes(self):
        piece_decorative.PS_DXF_jscode_fun('添加缩放定位点();')

    def count_materials(self):
        piece_decorative.PS_DXF_jscode_fun('信息写入();')

    def count_materials2(self):
        piece_decorative.PS_DXF3_jscode_fun('重写基码信息2();')
        piece_decorative.PS_DXF_jscode_fun('信息写入();')

if __name__ == '__main__':
    app2 = QApplication(sys.argv)
    dialog = ImportPDFDialog()
    dialog.show()
    sys.exit(app2.exec_())
