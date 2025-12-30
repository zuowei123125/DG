import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import piece_decorative
class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化界面
        self.init_ui()

    def init_ui(self):
        # 创建一个按钮
        btn = QPushButton('接口测试', self)

        # 连接按钮的点击事件到槽函数
        btn.clicked.connect(self.button_click)

        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 在布局中添加按钮
        layout.addWidget(btn)

        # 设置主窗口的布局
        self.setLayout(layout)

        # 设置主窗口的标题和大小
        self.setWindowTitle('测试')
        self.setGeometry(300, 300, 300, 200)

        # 显示界面
        self.show()

    def button_click(self):
        # 按钮点击时调用的槽函数

      #  piece_decorative.PS_DXF2_jscode_fun('设置花样组删除图层设置名称();')
      #  piece_decorative.PS_DXF12_jscode_fun('批量套数写入();')
        piece_decorative.PS_DXF2_jscode_fun('设置花样组2();')
        piece_decorative.PS_DXF19_jscode_fun('裁片抓取新的();')
        piece_decorative.PS_DXF2_jscode_fun('设置花样组顺序居中();')
        piece_decorative.PS_DXF_jscode_fun('信息写入();')
        piece_decorative.PS_DXF3_jscode_fun('裁片视图检查2();')
        print('按钮被点击了！')

if __name__ == '__main__':
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建主窗口
    window = SimpleApp()

    # 运行应用程序的主循环
    sys.exit(app.exec_())

