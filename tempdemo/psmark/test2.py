import myskin_styles, myskin_windows
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys, os
import piece_decorative
import ezdxf
import ezdxf.tools
import ezdxf.bbox
import ezdxf.units
import ezdxf.math
import qdarktheme

import re
def extract_number_from_block_name(block_name):
    # 使用正则表达式提取块名称中的数字部分
    match = re.search(r'P(\d+)', block_name)
    if match:
        return int(match.group(1))
    return 0  # 如果没有找到数字，默认返回0




def 获取dxf中心坐标和角度列表(doc):
    msp = doc.modelspace()
    mspBox = ezdxf.bbox.extents(msp)
    result = []
    for entity in msp.query():
        if entity.dxftype() == "INSERT":
            result.append({"块名称": entity.dxf.name, "center": None, "rotation": None})

            temp = []
            rotation = None
            block = doc.blocks[entity.dxf.name]
            for e in block:
                if e.dxftype() != "TEXT":
                    temp.append(e)
                else:
                    rotation = e.dxf.all_existing_dxf_attribs()["rotation"]
                    # 只有 0   90  -90 -180 出现其他的就以近似值代替
                    if rotation < 0:
                        rotation += 360
                    if rotation < 45 or rotation > 315:
                        rotation = 0
                    elif rotation < 135:
                        rotation = 90
                    elif rotation < 225:
                        rotation = -180
                    else:
                        rotation = -90

            result[-1]["rotation"] = rotation

            center = ezdxf.bbox.extents(temp).center
            # center y 改成从上往下计算
            center = (center.x, mspBox.size[1] + mspBox.extmin[1] - center.y)
            # 旋转
            center = (mspBox.size[1] - center[1], center[0])

            result[-1]["center"] = center

    # 打印处理前的数据
    print("处理前的数据：", result)

    # 按块名称进行排序
    result.sort(key=lambda x: extract_number_from_block_name(x["块名称"]))

    # 打印处理后的数据
    print("处理后的数据：", result)

    return result



class DXFWinUi(object):

    def setupUi(self, MainWindow):
        # MainWindow.resize(800, 600)

        self.centralwidget = QWidget(MainWindow)

        mainLayout = QHBoxLayout(self.centralwidget)

        groupBox = QGroupBox('多码混排')

        leftLayout = QVBoxLayout(groupBox)

        label1 = QLabel('大货裁片路径')
        # self.label2 = QLabel('暂未选择文件夹。')
        self.pushButton1 = QPushButton("选择文件夹")
        self.pushButton1.setFixedSize(100,30)
        leftLayout.addWidget(label1)
        # leftLayout.addWidget(self.label2)
        leftLayout.addWidget(self.pushButton1)
        leftLayout.addStretch()

        label6 = QLabel('DXF文件路径')
        # self.label7 = QLabel('暂未选择文件。')
        self.pushButton2 = QPushButton("选择文件")
        self.pushButton2.setFixedSize(100, 30)
        leftLayout.addWidget(label6)
        # leftLayout.addWidget(self.label7)
        leftLayout.addWidget(self.pushButton2)
        leftLayout.addStretch()


        label3 = QLabel('分辨率大小')
        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setValidator(QIntValidator())
        self.lineEdit1.setFixedSize(150,30)
        leftLayout.addWidget(label3)
        leftLayout.addWidget(self.lineEdit1)
        leftLayout.addStretch()

        label4 = QLabel('文档名称')
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setFixedSize(150,30)
        leftLayout.addWidget(label4)
        leftLayout.addWidget(self.lineEdit2)
        leftLayout.addStretch()

        label5 = QLabel('单码片数')
        self.lineEdit3 = QLineEdit()
        self.lineEdit3.setFixedSize(150,30)
        self.lineEdit3.setValidator(QIntValidator())
        leftLayout.addWidget(label5)
        leftLayout.addWidget(self.lineEdit3)
        leftLayout.addStretch()



        # 滚动区域
        scrollArea = QScrollArea()
        scrollArea.setFixedSize(200,210)
        scrollWidget = QWidget(scrollArea)
        self.scrollWidgetLayout = QVBoxLayout(scrollWidget)
        self.scrollWidgetLayout.setContentsMargins(5,5,5,5)
        self.scrollWidgetLayout.setSpacing(5)
        scrollArea.setWidget(scrollWidget)
        scrollArea.setWidgetResizable(True)
        leftLayout.addWidget(scrollArea)
        leftLayout.addStretch()

        rightWidget = QWidget()

        # rightLayout = QVBoxLayout(rightWidget)
        # self.okPushButton = QPushButton("OK")
        # self.cancelPushButton = QPushButton("Cancel")
        # rightLayout.addWidget(self.okPushButton)
        # rightLayout.addWidget(self.cancelPushButton)
        # rightLayout.addStretch()

        # rightWidget.setLayout(rightLayout)
        self.runButton = QPushButton("运行")
        leftLayout.addWidget(self.runButton)

        rightWidget = QWidget()

        mainLayout.addWidget(groupBox, 1)
      #  mainLayout.addWidget(rightWidget, 1)


        MainWindow.setCentralWidget(self.centralwidget)


class DXFWin(QMainWindow, DXFWinUi):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = DXFWinUi()
        self.ui.setupUi(self)
        self.setWindowTitle("水平布局管理例子")

        desktop = QApplication.desktop()
        self.move((desktop.width() - self.width()) / 2, (desktop.height() - self.height()) /2)

        self.ui.pushButton1.clicked.connect(self.chooseDir)
     #   self.ui.cancelPushButton.clicked.connect(self.close)
        self.ui.pushButton2.clicked.connect(self.chooseDxf)
      #  self.ui.okPushButton.clicked.connect(self.ok)
        self.ui.runButton.clicked.connect(self.run)

        self.dir = None
        self.dxfPath = None
        self.dxfLineEdits = {}

    def run(self):
        print("按钮被点击")

        pass



    def chooseDir(self):
        rst = QFileDialog.getExistingDirectory()

        if rst != '':
            self.ui.label2.setText(rst)
            self.dir = rst

    def chooseDxf(self):
        rst = QFileDialog.getOpenFileName(filter='dxf file(*.dxf)')
        rst = rst[0]

        if rst == '':
            return



        # 解析文件路径
   #     self.ui.label7.setText(rst)
        self.dxfPath = rst

        sizes = []
        temp = ''
        for c in os.path.basename(rst).split('.')[0]:
            import string
            if c in string.punctuation:
                if temp != '':
                    sizes.append(temp)
                    temp = ''
                continue
            temp += c
        if temp != '':
            sizes.append(temp)

        #清空self.ui.scrollWidgetLayout
        for i in range(self.ui.scrollWidgetLayout.count()):
            item = self.ui.scrollWidgetLayout.itemAt(0)
            self.ui.scrollWidgetLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
        self.dxfLineEdits = {}

        # 添加label和button
        for size in sizes:
            layout = QHBoxLayout()
            layout.addWidget(QLabel(size))
            layout.setContentsMargins(0,0,00,0)
            lineEdit = QLineEdit()
            lineEdit.setValidator(QIntValidator())
            lineEdit.setFixedSize(100, 30)
            self.dxfLineEdits[size] = lineEdit
            layout.addWidget(lineEdit)
            self.ui.scrollWidgetLayout.addLayout(layout)

    def ok(self):
        # 检查参数
        if self.dxfPath == None:
            QMessageBox.critical(self, "错误", "未选择dxf文件！")
            return
        if self.dir == None:
            QMessageBox.critical(self, "错误", "未选择大货裁片文件夹！")
            return

        # 禁用窗口
        self.setDisabled(True)

        # 解析dxf数据
        doc = ezdxf.readfile(self.dxfPath)
        msp = doc.modelspace()
        mspBox = ezdxf.bbox.extents(msp)

        画布高 = mspBox.size[0]
        画布宽 = mspBox.size[1]

        分辨率 = self.ui.lineEdit1.text()
        文档名称 = self.ui.lineEdit2.text()

        piece_decorative.PS_DXF21_jscode_fun(f'创建裁片排版文档({画布宽},{画布高},{分辨率},"{文档名称}");')
        单码片数 = int(self.ui.lineEdit3.text())
        DXFnames = []
        for size, lineEdit in self.dxfLineEdits.items():
            for i in range(单码片数):
                for j in range(int(lineEdit.text())):
                    DXFname = f"P{i + 1}-{size}"
                    DXFnames.append(DXFname)
        print(DXFnames)

        中心坐标和角度列表 = 获取dxf中心坐标和角度列表(doc)



        # 保存新的文件
      #  doc.saveas(self.dxfPath + ".out.dxf")

        for i in range(len(DXFnames)):
            DXFname = DXFnames[i]
            中心x_mm = 中心坐标和角度列表[i]["center"][0]
            中心y_mm = 中心坐标和角度列表[i]["center"][1]
            角度 = 中心坐标和角度列表[i]["rotation"]

            piece_decorative.PS_DXF21_jscode_fun(f'置入链接的智能对象("{self.dir}","{DXFname}");')
            piece_decorative.PS_DXF21_jscode_fun(f'裁片排版_lay({中心x_mm},{中心y_mm});')
            piece_decorative.PS_DXF21_jscode_fun(f'裁片角度({角度});')


        self.setDisabled(False)

def main():
    try:
        app = QApplication(sys.argv)
        # myskin_styles.dark(app)
        win = DXFWin()
        qdarktheme.setup_theme(
            custom_colors={
                "[dark]": {
                    "background": "#4d4d4d",
                    "foreground": "#ffffff",
                    "primary": "#ffffff",
                    "border": "#717070",
                }
            }
        )
        # mw = myskin_windows.ModernWindow(win)
       # win.setWindowIcon(QIcon('./ui/app.ico'))
        win.show()
        # win.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()