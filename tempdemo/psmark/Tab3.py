import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QGroupBox, QLabel, QLineEdit, QFormLayout
import piece_decorative

class ImportPDFDialog2(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Import Multiple PDF pages')

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)


        new_group_box5 = QGroupBox('打版联动')
        new_group_layout5 = QVBoxLayout(new_group_box5)

        # 创建4个按钮并连接到槽函数
        Dbtn4_1 = QPushButton('图层分割')
        Dbtn4_2 = QPushButton('批量图层编组')
        Dbtn4_3 = QPushButton('快速超链接')
     #   Dbtn4_4 = QPushButton('定位点比例缩放(模板)')

        Dbtn4_1.clicked.connect(self.on_Dbtn4_1_clicked)
        Dbtn4_2.clicked.connect(self.on_Dbtn4_2_clicked)
        Dbtn4_3.clicked.connect(self.on_Dbtn4_3_clicked)
       # Dbtn4_4.clicked.connect(self.on_Dbtn4_4_clicked)

        # 将按钮添加到新的盒子1中
        new_group_layout5.addWidget(Dbtn4_1)
        new_group_layout5.addWidget(Dbtn4_2)
        new_group_layout5.addWidget(Dbtn4_3)
      #  new_group_layout5.addWidget(Dbtn4_4)
        # 将新的盒子1添加到主布局中
        main_layout.addWidget(new_group_box5)





        # 快速换图
        quick_change_group = QGroupBox('快速换图')
        quick_change_layout = QVBoxLayout(quick_change_group)
        # bigbtn_standardize_pattern = QPushButton('图像切割')
        btn_standardize_pattern = QPushButton('花样标准化')

        btn_pattern_to_external = QPushButton('花样转外链')
        btn_quick_change = QPushButton('快速换图')
        btn_batch_quick_change = QPushButton('批量快速换图')
        # btn_Kbatch_quick_change = QPushButton('特定版本快速换图')
        # 为每个按钮连接槽函数
        btn_standardize_pattern.clicked.connect(self.on_standardize_pattern_clicked)
        btn_pattern_to_external.clicked.connect(self.on_pattern_to_external_clicked)
        btn_quick_change.clicked.connect(self.on_quick_change_clicked)
        btn_batch_quick_change.clicked.connect(self.on_batch_quick_change_clicked)
        # btn_Kbatch_quick_change.clicked.connect(self.on_kbatch_quick_change_clicked)
        # bigbtn_standardize_pattern.clicked.connect(self.on_bigstandardize_pattern_clicked)

        quick_change_layout.addWidget(btn_standardize_pattern)
        # quick_change_layout.addWidget(bigbtn_standardize_pattern)
        quick_change_layout.addWidget(btn_pattern_to_external)
        quick_change_layout.addWidget(btn_quick_change)
        quick_change_layout.addWidget(btn_batch_quick_change)
        # quick_change_layout.addWidget(btn_Kbatch_quick_change)

        main_layout.addWidget(quick_change_group)

        # 初始化界面

    # 创建一个新的盒子
        new_group_box1 = QGroupBox('模板生成')
        new_group_layout1 = QVBoxLayout(new_group_box1)

        # 创建4个按钮并连接到槽函数
        btn4_1 = QPushButton('通码延申(模板)')
        btn4_2 = QPushButton('宽高缩放(模板)')
        btn4_3 = QPushButton('比例缩放(模板)')
        btn4_4 = QPushButton('定位点比例缩放(模板)')

        btn4_1.clicked.connect(self.on_btn4_1_clicked)
        btn4_2.clicked.connect(self.on_btn4_2_clicked)
        btn4_3.clicked.connect(self.on_btn4_3_clicked)
        btn4_4.clicked.connect(self.on_btn4_4_clicked)

        # 将按钮添加到新的盒子1中
        new_group_layout1.addWidget(btn4_1)
        new_group_layout1.addWidget(btn4_2)
        new_group_layout1.addWidget(btn4_3)
        new_group_layout1.addWidget(btn4_4)
        # 将新的盒子1添加到主布局中
        main_layout.addWidget(new_group_box1)







#############################################

        new_group_box5 = QGroupBox('定位码快速换图')
        new_group_layout5 = QVBoxLayout(new_group_box5)

        # 创建4个按钮并连接到槽函数
        Kbtn4_1 = QPushButton('定位码快速超链接')
        Kbtn4_2 = QPushButton('定位码快速换图')

        #   Dbtn4_4 = QPushButton('定位点比例缩放(模板)')

        Kbtn4_1.clicked.connect(self.on_Kbtn4_1_clicked)
        Kbtn4_2.clicked.connect(self.on_Kbtn4_2_clicked)
        #Dbtn4_3.clicked.connect(self.on_Dbtn4_3_clicked)
        # Dbtn4_4.clicked.connect(self.on_Dbtn4_4_clicked)

        # 将按钮添加到新的盒子1中
        new_group_layout5.addWidget(Kbtn4_1)
        new_group_layout5.addWidget(Kbtn4_2)
       # new_group_layout5.addWidget(Dbtn4_3)
        #  new_group_layout5.addWidget(Dbtn4_4)
        # 将新的盒子1添加到主布局中
        main_layout.addWidget(new_group_box5)



 ##############################################

        new_group_box2 = QGroupBox('批量化工具')
        new_group_layout2 = QVBoxLayout(new_group_box2)

        # 创建4个按钮并连接到槽函数
        Pbtn4_1 = QPushButton('小码标添加')
        Pbtn4_2 = QPushButton('批量修改分辨率')
        Pbtn4_3 = QPushButton('批量加款号')
        Pbtn4_4 = QPushButton('模特批量替换')
        Pbtn4_5 = QPushButton('SO小样连晒')
        Pbtn4_6 = QPushButton('SO小样拼贴')
        Pbtn4_7 = QPushButton('SO小样缩放')

        Pbtn4_1.clicked.connect(self.on_Pbtn4_1_clicked)
        Pbtn4_2.clicked.connect(self.on_Pbtn4_2_clicked)
        Pbtn4_3.clicked.connect(self.on_Pbtn4_3_clicked)
        Pbtn4_4.clicked.connect(self.on_Pbtn4_4_clicked)
        Pbtn4_5.clicked.connect(self.on_Pbtn4_5_clicked)
        Pbtn4_6.clicked.connect(self.on_Pbtn4_6_clicked)
        Pbtn4_7.clicked.connect(self.on_Pbtn4_7_clicked)
        # 将按钮添加到新的盒子1中
        new_group_layout2.addWidget(Pbtn4_1)
        new_group_layout2.addWidget(Pbtn4_2)
        new_group_layout2.addWidget(Pbtn4_3)
        new_group_layout2.addWidget(Pbtn4_4)
        new_group_layout2.addWidget(Pbtn4_5)
        new_group_layout2.addWidget(Pbtn4_6)
        new_group_layout2.addWidget(Pbtn4_7)
        # 将新的盒子1添加到主布局中
        main_layout.addWidget(new_group_box2)

    # def on_kbatch_quick_change_clicked(self):
    #     piece_decorative.PS_DXF18_jscode_fun('龙服的快速换图();')
    #
    #     print("按钮被点击")
    #     pass

    def on_Pbtn4_7_clicked(self):
        piece_decorative.PS_DXF27_jscode_fun('新的米样缩放();')

        print("按钮被点击")
        pass


    def on_Kbtn4_1_clicked(self):
        piece_decorative.PS_DXF16_jscode_fun('快速定位码链接();')

        print("按钮被点击")
        pass


    def on_Kbtn4_2_clicked(self):
        piece_decorative.PS_DXF17_jscode_fun('定位码批量化替换外链新();')

        print("按钮被点击")
        pass




    def on_Dbtn4_1_clicked(self):
        piece_decorative.PS_DXF8_jscode_fun('图像分割();')

        print("按钮被点击")
        pass

    def on_Dbtn4_2_clicked(self):
        piece_decorative.PS_DXF15_jscode_fun('图层自动编组2();')

        print("按钮被点击")
        pass

    def on_Dbtn4_3_clicked(self):
        piece_decorative.PS_DXF15_jscode_fun('快速超级链接2();')
        # piece_decorative.PS_DXF22_jscode_fun('模特换衣功能();')
        print("按钮被点击")
        pass

    def on_Pbtn4_4_clicked(self):
        piece_decorative.PS_DXF26_jscode_fun('模特换图();')

        print("按钮被点击")
        pass

    def on_Pbtn4_5_clicked(self):
        piece_decorative.PS_DXF23_jscode_fun('自动连晒();')

        print("按钮被点击")
        pass

    def on_Pbtn4_6_clicked(self):
        piece_decorative.PS_DXF24_jscode_fun('自动米样拼贴();')

        print("按钮被点击")
        pass


    def on_Pbtn4_1_clicked(self):
        piece_decorative.PS_DXF8_jscode_fun('码标添加2();')

        print("按钮被点击")
        pass

    def on_Pbtn4_2_clicked(self):
        piece_decorative.PS_DXF8_jscode_fun('批量分辨率修改();')
        print("按钮被点击")
        pass


    def on_Pbtn4_3_clicked(self):
        piece_decorative.PS_DXF8_jscode_fun('批量款号添加();')
        print("按钮被点击")
        pass
    # 槽函数示例
    def on_standardize_pattern_clicked(self):
        piece_decorative.PS_DXF5_jscode_fun('花样标准化3();')
        print("花样标准化按钮被点击")


    def on_pattern_to_external_clicked(self):
        piece_decorative.PS_DXF5_jscode_fun('花样图层导出();')
        print("花样转外链按钮被点击")

    def on_quick_change_clicked(self):
        piece_decorative.PS_DXF5_jscode_fun('替换外链新();')
        print("快速换图按钮被点击")




    def on_batch_quick_change_clicked(self):
        piece_decorative.PS_DXF8_jscode_fun('批量化替换外链新();')
        print("批量快速换图按钮被点击")

    def on_btn4_1_clicked(self):
        # 处理新盒子1中按钮4_1的点击事件
        piece_decorative.PS_DXF_jscode_fun('删除指定名称蒙版();')
        piece_decorative.PS_DXF5_jscode_fun('裁片射出模板();')
        piece_decorative.PS_DXF2_jscode_fun('信息激活2();')
        pass

    def on_btn4_2_clicked(self):
        # 处理新盒子1中按钮4_2的点击事件
        piece_decorative.PS_DXF_jscode_fun('删除指定名称蒙版();')
        piece_decorative.PS_DXF4_jscode_fun('裁片射出宽高缩放模板();')
        piece_decorative.PS_DXF2_jscode_fun('信息激活2();')
        pass

    def on_btn4_3_clicked(self):
        # 处理新盒子1中按钮4_3的点击事件
        piece_decorative.PS_DXF_jscode_fun('删除指定名称蒙版();')
        piece_decorative.PS_DXF14_jscode_fun('裁片射出宽高缩放模板按中心();')
        piece_decorative.PS_DXF2_jscode_fun('信息激活2();')
        pass

    def on_btn4_4_clicked(self):
        # 处理新盒子1中按钮4_3的点击事件
        piece_decorative.PS_DXF_jscode_fun('删除指定名称蒙版();')
        piece_decorative.PS_DXF7_jscode_fun('裁片射出缩放模板();')
        piece_decorative.PS_DXF2_jscode_fun('信息激活2();')
        pass


    # def on_Dbtn4_1_clicked(self):
    #     # 处理新盒子1中按钮4_4的点击事件
    #     piece_decorative.PS_DXF8_jscode_fun('图像分割();')
    #     pass

    # def on_Pbtn4_5_clicked(self):
    #     # 处理新盒子1中按钮4_4的点击事件
    #     piece_decorative.PS_DXF11_jscode_fun('批量重设画布幅宽    ();')
    #     pass
    # def on_Pbtn4_6_clicked(self):
    #     # 处理新盒子1中按钮4_4的点击事件
    #     piece_decorative.PS_DXF11_jscode_fun('批量重设画布幅宽();')
    #     pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = ImportPDFDialog2()
    dialog.show()
    sys.exit(app.exec_())
