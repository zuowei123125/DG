import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Tab1 import ImportPDFDialog
from Tab2 import YourMainWindow
from Tab3 import ImportPDFDialog2
from Tab6 import ImportPDFDialog6
from Tab4 import ImportPDFDialog4
from test5 import YourMainWindow9
import qdarktheme
import sys
import subprocess
import re
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, \
    QSpacerItem, QSizePolicy, QMessageBox
import pymysql
import piece_decorative
import configparser

def exception_hook(exctype, value, traceback):
    # Handle the uncaught exception
    # 处理未捕获的异常
    QMessageBox.warning(None, "错误", f"发生了未知的异常：{value}")

# class LoginDialog(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("PSMARK登录界面")
#         self.setWindowIcon(QIcon("icons/newapp.ico"))  # 设置窗口小图标，替换为您的图标文件路径
#
#         self.resize(300, 200)
#
#         主布局 = QVBoxLayout()
#
#         group1 = QGroupBox("登录验证")
#         group1_layout = QVBoxLayout()
#
#         group2 = QHBoxLayout()
#         label1 = QLabel("用户名")
#         self.edit1 = QLineEdit()
#         self.edit1.setFixedWidth(200)
#         spacer1 = QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
#         group2.addWidget(label1)
#         group2.addItem(spacer1)
#         group2.addWidget(self.edit1)
#
#         group3 = QHBoxLayout()
#         label2 = QLabel("密码")
#         self.edit2 = QLineEdit()
#         self.edit2.setFixedWidth(200)
#         self.edit2.setEchoMode(QLineEdit.Password)  # 设置密码输入框为密文
#         spacer2 = QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
#         group3.addWidget(label2)
#         group3.addItem(spacer2)
#         group3.addWidget(self.edit2)
#
#
#
#         group4 = QHBoxLayout()
#         button1 = QPushButton("登录")
#         button2 = QPushButton("注册")
#         group4.addWidget(button1)
#         group4.addWidget(button2)
#
#         group1_layout.addLayout(group2)
#         group1_layout.addLayout(group3)
#         group1_layout.addLayout(group4)
#         group1.setLayout(group1_layout)
#
#         主布局.addWidget(group1)
#
#         group5 = QHBoxLayout()
#         label3 = QLabel("机器码")
#         self.edit3 = QLineEdit()
#         self.edit3.setFixedWidth(200)
#
#         # 获取主板序列号并提取数字部分
#         try:
#             result = subprocess.run(['wmic', 'baseboard', 'get', 'serialnumber'], stdout=subprocess.PIPE,
#                                     stderr=subprocess.PIPE, text=True)
#             motherboard_serial = result.stdout.strip()
#
#             # 使用正则表达式提取数字
#             motherboard_serial = re.sub(r'\D', '', motherboard_serial)
#
#             # 使用SHA-256加密特征码
#             feature_code = hashlib.sha256(motherboard_serial.encode()).hexdigest()
#
#             # 去掉特征码中的英文字符
#             feature_code = re.sub(r'[a-zA-Z]', '', feature_code)
#         except Exception as e:
#             feature_code = "Error: " + str(e)
#
#         self.edit3.setText(feature_code)  # 将加密后的特征码设置为 "特征码" 输入框的文本
#         self.rem_user()
#
#         spacer3 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
#         group5.addWidget(label3)
#         group5.addItem(spacer3)
#         group5.addWidget(self.edit3)
#
#         主布局.addLayout(group5)
#
#         self.setLayout(主布局)
#
#         # 链接登录的点击事件
#         button1.clicked.connect(self.slot_login)
#         # 连接注册按钮的点击事件
#         button2.clicked.connect(self.show_warning_message)
#
#     #记住密码
#     def rem_user(self):
#
#         piece_decorative.config = configparser.ConfigParser()
#         piece_decorative.config.read('config.ini', encoding='utf-8')
#         piece_decorative.PSname = piece_decorative.config.get('程序配置', 'PSname')
#         self.window = MainWindow()
#         self.window.show()
#         self.close()
#         return
#
#         code = self.edit3.text()
#         # 执行SQL语句，从user数据表中查询字段值
#         cur.execute(f"SELECT username,password,code FROM {User}")
#         # 将数据库查询的结果保存在result中
#         result = cur.fetchall()
#         code_list = [it[2] for it in result]  # 从数据库查询的result中遍历查询元组中第3个元素code
#         if code in code_list:
#             user_name = result[code_list.index(code)][0]
#             user_password = result[code_list.index(code)][1]
#             self.edit1.setText(user_name)
#             self.edit2.setText(user_password)
#         else:
#             pass
#
#     def slot_login(self):
#         user_name = self.edit1.text()
#         user_password = self.edit2.text()
#         code = self.edit3.text()
#         # print(user_name,user_password)
#         # 执行SQL语句，从user数据表中查询code和time字段值
#         cur.execute(f"SELECT username,password,code FROM {User}")
#         # 将数据库查询的结果保存在result中
#         result = cur.fetchall()
#         name_list = [it[0] for it in result]  # 从数据库查询的result中遍历查询元组中第一个元素name
#         # 判断用户名或密码不能为空
#         if not (user_name and user_password):
#             QMessageBox.critical(self, "错误", "用户名或密码不能为空！")
#             # 判断用户名和密码是否匹配
#         elif user_name in name_list:
#             if user_password == result[name_list.index(user_name)][1]:
#                 if code == result[name_list.index(user_name)][2]:
#                     piece_decorative.config = configparser.ConfigParser()
#                     piece_decorative.config.read('config.ini', encoding='utf-8')
#                     piece_decorative.PSname = piece_decorative.config.get('程序配置', 'PSname')
#                     self.window = MainWindow()
#                     self.window.show()
#                     self.close()
#                 else:
#                     QMessageBox.critical(self, "错误", "机器码不匹配！")
#                 # QMessageBox.information(self, "欢迎您", "登录成功！\n在此添加新界面！")
#             else:
#                 QMessageBox.critical(self, "错误", "密码输入错误！")
#         # 账号不在数据库中，则弹出是否注册的框
#         else:
#             QMessageBox.critical(self, "错误", "该账号不存在，请注册！")
#
#     def show_warning_message(self):
#         # 弹出警告消息框
#         QMessageBox.critical(self, "错误", "请联系管理员 17520145271！")
#         # warning_message = QMessageBox()
#         # warning_message.setIcon(QMessageBox.Warning)
#         # warning_message.setWindowTitle("警告")
#         # warning_message.setText("请联系管理员 17520145271")
#         # warning_message.exec_()

#################################自定义tab标签#################################
from PyQt5 import QtGui, QtCore, QtWidgets

class MyTabBar(QtWidgets.QTabBar):
    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()
        for index in range(self.count()):
            self.initStyleOption(option, index)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, option)
            painter.drawText(
                self.tabRect(index),
                QtCore.Qt.AlignCenter | QtCore.Qt.TextDontClip,
                "\n".join(self.tabText(index)))

    def tabSizeHint(self, index):
        #size = QtWidgets.QTabBar.tabSizeHint(self, index)
        width = max([QtWidgets.QTabBar.fontMetrics(self).width(text) for text in self.tabText(index)])
        height = len(self.tabText(index)) * QtWidgets.QTabBar.fontMetrics(self).lineSpacing()
        return QtCore.QSize(width + 12, height + 12)

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.setTabBar(MyTabBar())
#################################自定义tab标签#################################

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PS Mark")
        self.setWindowIcon(QIcon("icons/newapp.ico"))  # 设置窗口小图标，替换为您的图标文件路径

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        tab_widget = TabWidget()
        tab_widget.setTabPosition(TabWidget.West)
        #tab_widget.tabBar().setStyle(TabBarStyle(Qt.Vertical))
        main_layout.addWidget(tab_widget)

        tab2 = YourMainWindow()
        tab_widget.addTab(tab2, "纸样分割")

        tab1 = ImportPDFDialog()
        tab_widget.addTab(tab1, "裁片套版")
        #
        #
        tab3 = ImportPDFDialog2()
        tab_widget.addTab(tab3, "快速换图")

        # tab6 = ImportPDFDialog6()
        # tab_widget.addTab(tab6, "ai重绘")
        #
        # tab3 = YourMainWindow9()
        # tab_widget.addTab(tab3, "快速换图")

        # tab4 = ImportPDFDialog4()
        # tab_widget.addTab(tab4, "版本介绍")
        #
        # separator = QFrame()
        # separator.setFrameShape(QFrame.HLine)
        # separator.setFrameShadow(QFrame.Sunken)
        # main_layout.addWidget(separator)

        #custom_label = QLabel("尊敬的公司内部体验版用户(1.8.5)，欢迎使用！！！")
        #############8-12号修复了宽高缩放跟比例缩放超过10个裁片就会定位不准的bug
        #############8-12号将缩水值跟前缀添加改为了前置条件
        #############8-24号新增Tab2界面 将DXF解析与CDR结合在一起 可以实现分段排版


       # main_layout.addWidget(custom_label)

        self.setLayout(main_layout)
        # # self.setWindowTitle("分割线和自定义文字示例")
        # settings_button = QPushButton(QIcon("icons/转换.png"), "")

        # settings_button.setObjectName("settingsButton")  # 设置对象名称以供样式表选择
        # settings_button.setStyleSheet("border: none;")  # 设置按钮无边框
        # main_layout.addWidget(settings_button, alignment=Qt.AlignLeft)

        # 设置窗口始终置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.width_ratio = 0.3
        self.height_ratio = 1

        self.initial_width = self.width()
        self.initial_height = self.height()

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #
    #     # 获取当前窗口的宽度和高度
    #     current_width = self.width()
    #     current_height = self.height()
    #
    #     # 判断当前窗口是否超过了初始大小
    #     if current_width > self.initial_width or current_height > self.initial_height:
    #         # 允许窗口继续拉伸，不设置最小宽度和最小高度
    #         pass
    #     else:
    #         # 重新设置最小宽度和最小高度为初始大小
    #         self.setMinimumWidth(self.initial_width)
    #         self.setMinimumHeight(self.initial_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # 获取当前窗口的宽度和高度
        current_width = self.width()
        current_height = self.height()

        # 如果是第一次调整大小，更新初始大小
        if not hasattr(self, 'initial_size_set') or not self.initial_size_set:
            self.initial_width = current_width
            self.initial_height = current_height
            self.initial_size_set = True  # 标记初始大小已被设置

        # 判断当前窗口是否超过了初始大小
        if current_width > self.initial_width or current_height > self.initial_height:
            # 允许窗口继续拉伸，不设置最小宽度和最小高度
            pass
        else:
            # 重新设置最小宽度和最小高度为初始大小
            self.setMinimumWidth(self.initial_width)
            self.setMinimumHeight(self.initial_height)



if __name__ == '__main__':
    host = "rm-bp1s36ps814qp23b7uo.mysql.rds.aliyuncs.com"
    user = "zw1847930177"
    password = "Zuowei1216"
    database = "program"
    charset = "utf8"
    port = 3306
    db = pymysql.connect(host=host, user=user, password=password, database=database, charset=charset, port=port)
    cur = db.cursor()
    user_creat ="""
                    CREATE TABLE IF NOT EXISTS User(
                    `id` INT auto_increment PRIMARY KEY,
                    `username` varchar(255) DEFAULT '',
                    `password` varchar(255) DEFAULT '',
                    `code` varchar(255) DEFAULT ''
                    ) ENGINE=innodb DEFAULT CHARSET=utf8;
            """
    cur.execute(user_creat)
    cur = db.cursor()
    User = 'User'

    app3 = QApplication(sys.argv)
    sys.excepthook = exception_hook  # 设置全局异常处理

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
    # login_dialog = LoginDialog()
    # login_dialog.show()
    window = MainWindow()
    window.show()
    sys.exit(app3.exec_())
