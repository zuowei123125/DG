from flask import *

import os
import pymysql
import tempfile
import shutil
from zipfile import ZipFile
import datetime

#==================================================================================================

app = Flask(__name__)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "fo847543jfrgowjfa8otu43"

#==================================================================================================
def get_connect():
    host = "rm-bp1s36ps814qp23b7uo.mysql.rds.aliyuncs.com"
    user = "zw1847930177"
    password = "Zuowei1216"
    database = "program"
    charset = "utf8"
    port = 3306
    conn = pymysql.connect(host=host, user=user, password=password, database=database, charset=charset, port=port)
    return conn

def getallusers():
    try:
        conn = get_connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(f'select * from user;')
        user_data = cur.fetchall()
        return user_data

    finally:
        cur.close()
        conn.close()

def new_users(username, password, code):
    conn = get_connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f"""INSERT INTO `program`.`user` (`username`, `password`, `code`, `expiredate`) VALUES ('{username}', '{password}', '{code}', '{(datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")}');""")
    conn.commit()


#==================================================================================================

def 无code():
    userinfo_filepath = os.path.join("tmp", "userinfo.txt")
    with open(userinfo_filepath, 'w') as f:
        f.write("error")
    with ZipFile(os.path.join("tmp", 'result.zip'), 'w') as z:
        z.write(userinfo_filepath, arcname="userinfo.txt")

    return send_from_directory("tmp", "result.zip", as_attachment=True)

def 错误的用户名或密码():
    userinfo_filepath = os.path.join("tmp", "userinfo.txt")
    with open(userinfo_filepath, 'w') as f:
        f.write("error")
    with ZipFile(os.path.join("tmp", 'result.zip'), 'w') as z:
        z.write(userinfo_filepath, arcname="userinfo.txt")
    return send_from_directory("tmp", "result.zip", as_attachment=True)

#==================================================================================================
def 返回正常数据(username, password):

    userinfo_filepath = os.path.join("tmp", "userinfo.txt")
    with open(userinfo_filepath, 'w', encoding='utf-8') as f:
        f.write(f"{username}\n{password}")

    with open("using.txt", 'r') as f:
        shutil.copyfile(f"archives/{f.read()}.zip", os.path.join("tmp", "data.zip"))

    with ZipFile(os.path.join("tmp", 'result.zip'), 'w') as z:
        z.write(userinfo_filepath, arcname="userinfo.txt")
        z.write(os.path.join("tmp", "data.zip"), arcname="data.zip")

    return send_from_directory("tmp", "result.zip", as_attachment=True)


#==================================================================================================
@app.route("/query", methods=["POST"])
def query():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    code = request.args.get("code", "")

    allusers = getallusers()

    if code == "":
        return 无code()

    if username == "" and password == "":
        for user in allusers:
            if code == user["code"] and (user["expiredate"] - datetime.datetime.now()).total_seconds() > 0:
                return 返回正常数据(user["username"], user["password"])
    else:
        for user in allusers:
            if username == user["username"] and password == user["password"] and code == user["code"]  and (user["expiredate"] - datetime.datetime.now()).total_seconds() > 0:
                return 返回正常数据(user["username"], user["password"])

    return 错误的用户名或密码()

#==================================================================================================
# 设置使用的档案
@app.route("/set_using_archives", methods=["POST"])
def set_using_archives():
    # 检查权限
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if not (username == ADMIN_USERNAME and password == ADMIN_PASSWORD):
        abort(403)

    result = request.form.get("result")

    if result not in [os.path.basename(a).split('.')[0] for a in os.listdir("archives")]:
        return 'error'

    with open("using.txt", 'w') as f:
        f.write(result)

    return 'OK'
#==================================================================================================
# 获取正在使用的档案名称
@app.route("/get_using_archives_name", methods=["GET"])
def get_using_archives_name():
    with open("using.txt", 'r') as f:
        return f.read()
#==================================================================================================
# 注册
@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        code = request.form.get("code")
        adminpassword = request.form.get("adminpassword")

        with open("adminpassword.txt", 'r') as f:
            true_adminpassword = f.read().strip()

        if adminpassword != true_adminpassword:
            return "error"

        else:
            new_users(username, password, code)
            return 'success'

#==================================================================================================
@app.route("/archives", methods=["GET", "POST"])
def archives():
    if request.method == "GET":
        # 获取档案列表
        archives = os.listdir("archives")
        archives = [os.path.basename(a).split(".")[0] for a in archives]
        return jsonify(archives)

    elif request.method == "POST":
        # 上传档案
        username = request.form.get("username")
        password = request.form.get("password")

        if not (username == ADMIN_USERNAME and password == ADMIN_PASSWORD):
            abort(403)

        file = request.files['file']
        file.save(f"./archives/{str(datetime.datetime.now()).split('.')[0].replace(':', '')}.zip")

        return 'OK'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)


