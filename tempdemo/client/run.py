import os
import shutil
import sys
import tempfile
import time
import wmi
import psutil
import threading
import qtpy, platform
import winreg
from qtpy.QtCore import Qt, QMetaObject, Signal, Slot, QEvent
from qtpy.QtWidgets import QWidget, QVBoxLayout, QInputDialog, QHBoxLayout, QToolButton, QLabel, QSizePolicy, QSplashScreen
from PyQt5.QtGui import QIcon, QPixmap
import re
import hashlib
import configparser
from win32com.client import Dispatch
import ezdxf
import zipfile
import PyQt5
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import qdarktheme
import sys
import subprocess
import re
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, \
    QSpacerItem, QSizePolicy, QMessageBox
import pymysql
import requests

BASE_URL = "http://43.134.82.18/psmark"
#BASE_URL = "http://127.0.0.1:5001"

tempdir = ""

def exception_hook(exctype, value, traceback):
    # Handle the uncaught exception
    # 处理未捕获的异常
    QMessageBox.warning(None, "错误", f"发生了未知的异常：{value}")


class LoginDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSMARK登录界面")
        self.setWindowIcon(QIcon("icons/newapp.ico"))  # 设置窗口小图标，替换为您的图标文件路径

        self.resize(300, 200)

        主布局 = QVBoxLayout()

        group1 = QGroupBox("登录验证")
        group1_layout = QVBoxLayout()

        group2 = QHBoxLayout()
        label1 = QLabel("用户名")
        self.edit1 = QLineEdit()
        self.edit1.setFixedWidth(200)
        spacer1 = QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        group2.addWidget(label1)
        group2.addItem(spacer1)
        group2.addWidget(self.edit1)

        group3 = QHBoxLayout()
        label2 = QLabel("密码")
        self.edit2 = QLineEdit()
        self.edit2.setFixedWidth(200)
        self.edit2.setEchoMode(QLineEdit.Password)  # 设置密码输入框为密文
        spacer2 = QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        group3.addWidget(label2)
        group3.addItem(spacer2)
        group3.addWidget(self.edit2)

        group4 = QHBoxLayout()
        button1 = QPushButton("登录")
        button2 = QPushButton("注册")
        group4.addWidget(button1)
        group4.addWidget(button2)

        group1_layout.addLayout(group2)
        group1_layout.addLayout(group3)
        group1_layout.addLayout(group4)
        group1.setLayout(group1_layout)

        主布局.addWidget(group1)

        group5 = QHBoxLayout()
        label3 = QLabel("机器码")
        self.edit3 = QLineEdit()
        self.edit3.setFixedWidth(200)
        self.edit3.setReadOnly(True)
        self.edit3.setFocusPolicy(Qt.NoFocus)

        # 获取主板序列号并提取数字部分
        '''try:
            result = subprocess.run(['wmic', 'baseboard', 'get', 'serialnumber'], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True)
            motherboard_serial = result.stdout.strip()

            # 使用正则表达式提取数字
            motherboard_serial = re.sub(r'\D', '', motherboard_serial)

            # 使用SHA-256加密特征码
            feature_code = hashlib.sha256(motherboard_serial.encode()).hexdigest()

            # 去掉特征码中的英文字符
            feature_code = re.sub(r'[a-zA-Z]', '', feature_code)
        except Exception as e:
            feature_code = "Error: " + str(e)'''
        # 计算序列号

        try:
            feature_code = self.get_computer_code()
            count = ord(feature_code[0]) + ord(feature_code[1])
            for _ in range(count):
                feature_code = hashlib.md5(feature_code.encode()).hexdigest().upper()

        except Exception as e:
            feature_code = "Error: " + str(e)

        self.edit3.setText(feature_code)  # 将加密后的特征码设置为 "特征码" 输入框的文本
        self.rem_user()

        spacer3 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        group5.addWidget(label3)
        group5.addItem(spacer3)
        group5.addWidget(self.edit3)

        主布局.addLayout(group5)

        self.setLayout(主布局)

        # 链接登录的点击事件
        button1.clicked.connect(self.slot_login)
        # 连接注册按钮的点击事件
        button2.clicked.connect(self.register)

    def get_computer_code(self):
        computer_code = ''
        c = wmi.WMI()
        for cpu in c.Win32_Processor():
            computer_code += cpu.ProcessorId.strip()

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\SQMClient", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        # 读取设备ID
        computer_code += winreg.QueryValueEx(key, "MachineId")[0].strip()
        # 关闭注册表
        winreg.CloseKey(key)

        computer_code += str(subprocess.check_output('wmic csproduct get uuid').split(b'\n')[1].strip())

        return computer_code

    def register(self):

        dialog = RegisterDialog()
        if dialog.exec() != QDialog.Accepted:
            return

        r = requests.post(BASE_URL + f"/register", data={
            "username":dialog.get用户名(),
            "password":dialog.get密码(),
            "code":self.edit3.text(),
            "adminpassword":"qwe123456",
            "truename":dialog.get姓名(),
            "phone":dialog.get手机号(),
            "company":dialog.get公司名(),
            "address":dialog.get地址(),
        })

        if r.text == "success":
            QMessageBox.information(self, "成功", "注册成功！")

        elif r.text == 'exist':
            QMessageBox.critical(self, "错误", "用户已存在！")

        else:
            QMessageBox.critical(self, "错误", f"注册失败！{r.text}")

    #记住密码
    def rem_user(self):
        global tempdir
        code = self.edit3.text()

        r = requests.post(BASE_URL + f"/query?code={code}")
        with tempfile.TemporaryDirectory() as d:
            dname = d
        tempdir = dname + str(time.time())
        os.makedirs(tempdir)

        filepath = os.path.join(tempdir, "result.zip")
        with open(filepath, 'wb') as f:
            f.write(r.content)

        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(tempdir)

        with open(os.path.join(tempdir, "userinfo.txt"), 'r', encoding="utf-8") as f:
            userinfo = f.read()

        if userinfo == 'error':
            return

        self.edit1.setText(userinfo.split("\n")[0])
        self.edit2.setText(userinfo.split("\n")[1])

    def slot_login(self):
        global tempdir
        user_name = self.edit1.text()
        user_password = self.edit2.text()
        code = self.edit3.text()

        # 判断缓存是否存在
        with open(os.path.join(tempdir, "userinfo.txt"), 'r', encoding="utf-8") as f:
            userinfo = f.read()
        if not (userinfo.split("\n")[0] == user_name and userinfo.split("\n")[1] == user_password):
            r = requests.post(BASE_URL + f"/query?code={code}&username={user_name}&password={user_password}")
            with tempfile.TemporaryDirectory() as d:
                dname = d
            tempdir = dname + str(time.time())
            os.makedirs(tempdir)

            filepath = os.path.join(tempdir, "result.zip")
            with open(filepath, 'wb') as f:
                f.write(r.content)

            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(tempdir)

            with open(os.path.join(tempdir, "userinfo.txt"), 'r', encoding="utf-8") as f:
                userinfo = f.read()

            if userinfo == 'error':
                QMessageBox.critical(self, "错误", "机器码或账号密码错误！")
                return

        with zipfile.ZipFile(os.path.join(tempdir, "data.zip"), 'r') as zip_ref:
            zip_ref.extractall(tempdir)

        #print(tempdir)

        cwd = os.getcwd()
        sys.path.insert(0, tempdir)
        os.chdir(tempdir)

        import piece_decorative
        piece_decorative.config = configparser.ConfigParser()

        os.chdir(cwd)
        piece_decorative.config.read('config.ini', encoding='utf-8')
        piece_decorative.PSname = piece_decorative.config.get('程序配置', 'PSname')
        os.chdir(tempdir)

        import newMark
        #self.hide()
        self.window = newMark.MainWindow()
        self.window.show()
        self.close()
        #print("run")
        #newMark.run()


    def show_warning_message(self):
        # 弹出警告消息框
        QMessageBox.critical(self, "错误", "请联系管理员 17520145271！")
        # warning_message = QMessageBox()
        # warning_message.setIcon(QMessageBox.Warning)
        # warning_message.setWindowTitle("警告")
        # warning_message.setText("请联系管理员 17520145271")
        # warning_message.exec_()

from PyQt5.QtWidgets import QDialogButtonBox, QFormLayout
from PyQt5.QtGui import QIntValidator
import re
class RegisterDialog(QDialog):
    '''注册对话框'''
    def __init__(self):
        super(RegisterDialog,self).__init__()
        self.init_gui()

    def init_gui(self):
        #设置dialog窗口标题
        self.setWindowTitle("注册")
        # 设置界面尺寸大小
        self.resize(500, 260)

        self.用户名QLineEdit = QLineEdit()
        self.密码QLineEdit = QLineEdit()
        self.密码QLineEdit.setEchoMode(QLineEdit.Password)
        self.确认密码QLineEdit = QLineEdit()
        self.确认密码QLineEdit.setEchoMode(QLineEdit.Password)
        self.姓名QLineEdit = QLineEdit()
        self.手机号QLineEdit = QLineEdit()
        #self.手机号QLineEdit.setValidator(QIntValidator())
        self.公司名QLineEdit = QLineEdit()
        self.地址QLineEdit = QLineEdit()

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.check)
        self.buttons.rejected.connect(self.reject)

        # 表单布局，当然也可以使用其它布局方式
        layout = QFormLayout(self)
        layout.addRow('用户名(用于登录):', self.用户名QLineEdit)
        layout.addRow('密码(用于登录):', self.密码QLineEdit)
        layout.addRow('确认密码:', self.确认密码QLineEdit)
        layout.addRow('姓名:', self.姓名QLineEdit)
        layout.addRow('手机号(+86):', self.手机号QLineEdit)
        layout.addRow('公司名:', self.公司名QLineEdit)
        layout.addRow('地址:', self.地址QLineEdit)
        layout.addRow(self.buttons)

    def get用户名(self):
        return self.用户名QLineEdit.text().strip()

    def get密码(self):
        return self.密码QLineEdit.text().strip()

    def get确认密码(self):
        return self.确认密码QLineEdit.text().strip()

    def get姓名(self):
        return self.姓名QLineEdit.text().strip()

    def get手机号(self):
        return self.手机号QLineEdit.text().strip()

    def get公司名(self):
        return self.公司名QLineEdit.text().strip()

    def get地址(self):
        return self.地址QLineEdit.text().strip()

    def check(self):
        if self.get用户名() == '' or self.get密码() == '' or self.get姓名() == '' or self.get手机号() == '' or self.get公司名() == '' or self.get地址() == '':
            QMessageBox.critical(self, "错误", "信息不完整！")
            return

        if self.get密码() != self.get确认密码():
            QMessageBox.critical(self, "错误", "两次密码不一致！")
            return

        t = re.compile(r'[1-9][0-9]{10}')
        s = re.search(t, self.get手机号())
        if (not s) or (not self.get手机号().startswith('1')) or (len(self.get手机号()) != 11):
            QMessageBox.critical(self, "错误", "手机号格式错误！")
            return

        self.accept()


def main():

    app3 = QApplication(sys.argv)
    sys.excepthook = exception_hook  # 设置全局异常处理

    splash = QSplashScreen()
    splash.setPixmap(QPixmap('./splash.png'))
    splash.show()
    app3.processEvents()

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
    login_dialog = LoginDialog()
    login_dialog.show()
    splash.finish(login_dialog)  # 启动画面完成启动
    # window = MainWindow()
    # window.show()
    r = app3.exec_()
    time.sleep(1)
    os.chdir("C:")
    try:
        if tempdir != "":
            shutil.rmtree(tempdir, ignore_errors=True)
            #print("temp dir remove ok:", tempdir)
    except Exception as e:
        print(e)

    sys.exit(r)


if __name__ == '__main__':
    main()


