import sys
import subprocess
import re
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, \
    QSpacerItem, QSizePolicy, QMessageBox
import pymysql
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
                  `password` varchar(255) DEFAULT ''
                ) ENGINE=innodb DEFAULT CHARSET=utf8;
           """
cur.execute(user_creat)
cur = db.cursor()
User = 'User'

class LoginDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSMARK登录界面")
        self.resize(300, 200)

        主布局 = QVBoxLayout()

        group1 = QGroupBox("登录验证")
        group1_layout = QVBoxLayout()

        group2 = QHBoxLayout()
        label1 = QLabel("用户名")
        self.edit1 = QLineEdit()
        self.edit1.setFixedWidth(120)
        spacer1 = QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        group2.addWidget(label1)
        group2.addItem(spacer1)
        group2.addWidget(self.edit1)

        group3 = QHBoxLayout()
        label2 = QLabel("密码")
        self.edit2 = QLineEdit()
        self.edit2.setFixedWidth(120)
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
        edit3 = QLineEdit()
        edit3.setFixedWidth(200)

        # 获取主板序列号并提取数字部分
        try:
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
            feature_code = "Error: " + str(e)

        edit3.setText(feature_code)  # 将加密后的特征码设置为 "特征码" 输入框的文本

        spacer3 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        group5.addWidget(label3)
        group5.addItem(spacer3)
        group5.addWidget(edit3)

        主布局.addLayout(group5)

        self.setLayout(主布局)

        # 链接登录的点击事件
        button1.clicked.connect(self.slot_login)
        # 连接注册按钮的点击事件
        button2.clicked.connect(self.show_warning_message)

    def slot_login(self):
        user_name = self.edit1.text()
        user_password = self.edit2.text()
        # print(user_name,user_password)
        # 执行SQL语句，从user数据表中查询code和time字段值
        cur.execute(f"SELECT username,password FROM {User}")
        # 将数据库查询的结果保存在result中
        result = cur.fetchall()
        name_list = [it[0] for it in result]  # 从数据库查询的result中遍历查询元组中第一个元素name
        # 判断用户名或密码不能为空
        if not (user_name and user_password):
            QMessageBox.critical(self, "错误", "用户名或密码不能为空！")
            # 判断用户名和密码是否匹配
        elif user_name in name_list:
            if user_password == result[name_list.index(user_name)][1]:
                QMessageBox.information(self, "欢迎您", "登录成功！\n在此添加新界面！")
            else:
                QMessageBox.critical(self, "错误", "密码输入错误！")
        # 账号不在数据库中，则弹出是否注册的框
        else:
            QMessageBox.critical(self, "错误", "该账号不存在，请注册！")

    def show_warning_message(self):
        # 弹出警告消息框
        warning_message = QMessageBox()
        warning_message.setIcon(QMessageBox.Warning)
        warning_message.setWindowTitle("警告")
        warning_message.setText("请联系管理员 17520145271")
        warning_message.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    login_dialog.show()
    sys.exit(app.exec_())
