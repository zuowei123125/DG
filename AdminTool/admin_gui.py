import sys
import os
import requests
import subprocess
import paramiko
import shutil
import zipfile
from datetime import datetime
import json

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTabWidget, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QFileDialog, QGroupBox,
                             QComboBox, QDialog, QFormLayout, QDialogButtonBox,
                             QSplitter, QFrame, QListWidget, QListWidgetItem,
                             QInputDialog, QGridLayout, QTextEdit, QCheckBox,
                             QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QColor

from qfluentwidgets import (
    FluentWindow, FluentIcon, NavigationItemPosition, SplashScreen,
    FluentTranslator, QConfig, 
    PushButton, PrimaryPushButton, LineEdit, PasswordLineEdit,
    TextEdit, PlainTextEdit, ProgressBar, IndeterminateProgressBar,
    ComboBox, CheckBox, SwitchButton, Slider,
    CardWidget, SimpleCardWidget, HeaderCardWidget,
    TableWidget, ListWidget, 
    InfoBar, MessageBox, MessageBoxBase,
    BodyLabel, TitleLabel, SubtitleLabel, StrongBodyLabel, CaptionLabel,
    ScrollArea, PipsPager, TransparentToolButton
)

# Configuration
DEFAULT_API_URL = " https://backend.aidg168.uk/api/v1"
DEFAULT_ADMIN_TOKEN = "admin-secret-token"

class DatabaseManager:
    """管理 app_deployments 的版本信息（使用 SSH + JSON 文件）"""
    def __init__(self, config_path='deploy_config.json', db_type='frontend'):
        self.config = self.load_config(config_path)
        self.ssh = None
        self.sftp = None
        self.db_type = db_type
        if db_type == 'backend':
            self.remote_db_file = '/root/server_versions/.deployments.json'
        else:
            self.remote_db_file = '/var/www/app_versions/.deployments.json'
        
    def load_config(self, config_path):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置失败: {e}")
            return None
    
    def connect_ssh(self):
        """连接 SSH"""
        if self.ssh and self.ssh.get_transport() and self.ssh.get_transport().is_active():
            return
        
        if not self.config:
            raise Exception("配置文件不存在")
        
        import paramiko
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            hostname=self.config['host'],
            port=int(self.config.get('port', 22)),
            username=self.config['username'],
            password=self.config['password'],
            timeout=10
        )
        self.sftp = self.ssh.open_sftp()
    
    def get_deployments_data(self):
        """从服务器读取部署记录"""
        try:
            self.connect_ssh()
            
            # 尝试读取远程文件
            try:
                with self.sftp.open(self.remote_db_file, 'r') as f:
                    content = f.read().decode('utf-8')
                    return json.loads(content)
            except IOError:
                # 文件不存在，返回空数据
                return {'deployments': []}
        except Exception as e:
            raise Exception(f"读取部署记录失败: {e}")
    
    def save_deployments_data(self, data):
        """保存部署记录到服务器"""
        try:
            self.connect_ssh()
            
            # 确保目录存在
            if self.db_type == 'backend':
                self.ssh.exec_command('mkdir -p /root/server_versions')
            else:
                self.ssh.exec_command('mkdir -p /var/www/app_versions')
            
            # 写入文件
            with self.sftp.open(self.remote_db_file, 'w') as f:
                f.write(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            raise Exception(f"保存部署记录失败: {e}")
    
    def close(self):
        """关闭连接"""
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()
    
    def init_table(self):
        """初始化（确保文件存在）"""
        try:
            data = self.get_deployments_data()
            return True
        except:
            # 创建空文件
            self.save_deployments_data({'deployments': []})
            return True
    
    def add_deployment(self, version, file_size_mb=None, comment=None):
        """添加新部署记录"""
        try:
            data = self.get_deployments_data()
            
            # 将所有记录设为非当前
            for dep in data['deployments']:
                dep['is_current'] = False
            
            # 添加新记录
            new_dep = {
                'version': version,
                'deployed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'is_current': True,
                'file_size_mb': file_size_mb,
                'comment': comment
            }
            data['deployments'].append(new_dep)
            
            self.save_deployments_data(data)
            return True
        except Exception as e:
            raise Exception(f"添加部署记录失败: {e}")
    
    def get_all_deployments(self):
        """获取所有部署记录"""
        try:
            data = self.get_deployments_data()
            # 按时间倒序排序
            deployments = sorted(data['deployments'], key=lambda x: x['deployed_at'], reverse=True)
            return deployments
        except Exception as e:
            raise Exception(f"获取部署记录失败: {e}")
    
    def set_current_version(self, version):
        """设置当前版本"""
        try:
            data = self.get_deployments_data()
            
            # 更新状态
            for dep in data['deployments']:
                dep['is_current'] = (dep['version'] == version)
            
            self.save_deployments_data(data)
            return True
        except Exception as e:
            raise Exception(f"设置当前版本失败: {e}")
    
    def delete_deployment(self, version):
        """删除部署记录"""
        try:
            data = self.get_deployments_data()
            
            # 移除指定版本
            data['deployments'] = [d for d in data['deployments'] if d['version'] != version]
            
            self.save_deployments_data(data)
            return True
        except Exception as e:
            raise Exception(f"删除部署记录失败: {e}")

class ApiClient:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip("/")
        self.token = token
        
    def get_headers(self):
        return {"x-admin-token": self.token}

    def list_groups(self):
        try:
            resp = requests.get(f"{self.base_url}/admin/groups", headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"获取组列表失败: {str(e)}")

    def create_group(self, name, comment):
        try:
            payload = {"name": name, "comment": comment}
            resp = requests.post(f"{self.base_url}/admin/groups", json=payload, headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"创建组失败: {str(e)}")

    def upload_version(self, file_path):
        try:
            filename = os.path.basename(file_path)
            files = {'file': (filename, open(file_path, 'rb'))}
            data = {'token': self.token}
            resp = requests.post(f"{self.base_url}/admin/upload_version", files=files, data=data)
            resp.raise_for_status()
            return resp.json().get("filename")
        except Exception as e:
            raise Exception(f"上传失败: {str(e)}")

    def list_archives(self):
        try:
            resp = requests.get(f"{self.base_url}/admin/archives", headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"获取归档列表失败: {str(e)}")

    def update_group_version(self, group_id, filename):
        try:
            payload = {"current_version_file": filename}
            resp = requests.put(f"{self.base_url}/admin/groups/{group_id}", json=payload, headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"更新组版本失败: {str(e)}")
    
    def update_group_comment(self, group_id, comment):
        try:
            payload = {"comment": comment}
            resp = requests.put(f"{self.base_url}/admin/groups/{group_id}", json=payload, headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"更新组备注失败: {str(e)}")

    def list_users(self):
        try:
            resp = requests.get(f"{self.base_url}/admin/users", headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"获取用户列表失败: {str(e)}")

    def update_user_group(self, user_id, group_id):
        try:
            # group_id is query param in backend
            resp = requests.put(f"{self.base_url}/admin/users/{user_id}/group?group_id={group_id}", headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"更新用户组失败: {str(e)}")
            
    def update_user_permissions(self, user_id, permissions):
        try:
            data = {"permissions": permissions}
            resp = requests.put(f"{self.base_url}/admin/users/{user_id}/permissions", data=data, headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"更新用户权限失败: {str(e)}")

class CreateGroupDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("创建新组", self)
        
        self.name_edit = LineEdit()
        self.name_edit.setPlaceholderText("请输入组名称")
        self.name_edit.setClearButtonEnabled(True)
        
        self.comment_edit = LineEdit()
        self.comment_edit.setPlaceholderText("备注信息 (可选)")
        
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(StrongBodyLabel("组名称:", self))
        self.viewLayout.addWidget(self.name_edit)
        self.viewLayout.addWidget(StrongBodyLabel("备注:", self))
        self.viewLayout.addWidget(self.comment_edit)
        
        self.yesButton.setText("创建")
        self.cancelButton.setText("取消")
        
        self.widget.setMinimumWidth(350)
        
    def get_data(self):
        return self.name_edit.text(), self.comment_edit.text()

class SimpleInputDialog(MessageBoxBase):
    def __init__(self, title, label, default_text="", parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(title, self)
        self.input_edit = LineEdit()
        self.input_edit.setText(default_text)
        self.input_edit.setClearButtonEnabled(True)
        
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(StrongBodyLabel(label, self))
        self.viewLayout.addWidget(self.input_edit)
        
        self.yesButton.setText("确定")
        self.cancelButton.setText("取消")
        
        self.widget.setMinimumWidth(350)
        
    def get_text(self):
        return self.input_edit.text()

# Import config interface
from config_interface import ConfigInterface

class AdminWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DesignerCEP 管理工具")
        self.resize(1100, 750)
        
        # 启用 Mica 效果 (Win11)
        self.setMicaEffectEnabled(True)
        
        self.api_client = None
        self.groups_data = [] # Cache groups
        self.users_data = []  # Cache users
        self.db_manager = DatabaseManager(db_type='frontend')  # 前端版本数据库管理器
        self.db_initialized = False  # 前端数据库是否已初始化
        self.backend_db_manager = DatabaseManager(db_type='backend')  # 后端版本数据库管理器
        self.backend_db_initialized = False  # 后端数据库是否已初始化
        
        # 创建子界面
        self.home_interface = QWidget()
        self.manage_interface = QWidget() 
        self.release_interface = QWidget()
        self.deploy_interface = QWidget()
        self.config_interface = ConfigInterface(self.api_client, self) # Config Interface

        # 初始化旧版界面逻辑 (迁移到新容器)
        # 注意：为了快速迁移，我们保留旧的 setup_ 方法，但将其 parent 指向新界面
        self.setup_manage_tab_legacy(self.manage_interface)
        self.setup_release_tab_legacy(self.release_interface)
        self.setup_deploy_tab_legacy(self.deploy_interface)
        
        # 初始化 Home (连接页)
        self.setup_home_interface(self.home_interface)

        # 设置 ObjectName (FluentWindow 要求)
        self.home_interface.setObjectName("home_interface")
        self.manage_interface.setObjectName("manage_interface")
        self.release_interface.setObjectName("release_interface")
        self.deploy_interface.setObjectName("deploy_interface")
        self.config_interface.setObjectName("config_interface")

        # 添加导航项
        self.addSubInterface(self.home_interface, FluentIcon.HOME, "首页连接")
        self.addSubInterface(self.manage_interface, FluentIcon.PEOPLE, "组与用户")
        self.addSubInterface(self.release_interface, FluentIcon.CLOUD, "发布上传")
        self.addSubInterface(self.deploy_interface, FluentIcon.SEND, "自动部署")
        
        self.addSubInterface(
            self.config_interface,
            FluentIcon.SETTING,
            "系统配置",
            NavigationItemPosition.BOTTOM
        )
        
        # 自动连接
        self.init_connection()

    def setup_home_interface(self, widget):
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 标题
        layout.addWidget(TitleLabel("欢迎使用 DesignerCEP 管理工具", widget))
        layout.addWidget(BodyLabel("请先连接到后端服务器以开始管理。", widget))
        
        layout.addSpacing(20)

        # 连接卡片
        card = HeaderCardWidget("服务器连接")
        
        # 使用 Grid 布局在卡片内部
        # HeaderCardWidget 的 viewLayout 是 content 部分的布局
        # 但我们通常直接给 card 设布局，或者使用 SimpleCardWidget
        # 这里为了简单，我们自定义一个带边框的容器或者直接用 GroupBox 但改样式
        # 为了最佳效果，我们使用 SimpleCardWidget
        
        # 这里重新设计：
        # 一个大卡片包含连接信息
        
        conn_card = SimpleCardWidget(widget)
        conn_layout = QGridLayout(conn_card)
        conn_layout.setContentsMargins(20, 20, 20, 20)
        conn_layout.setSpacing(15)
        
        conn_layout.addWidget(StrongBodyLabel("API 地址:"), 0, 0)
        self.url_edit = LineEdit()
        self.url_edit.setText(DEFAULT_API_URL)
        self.url_edit.setClearButtonEnabled(True)
        conn_layout.addWidget(self.url_edit, 0, 1)
        
        conn_layout.addWidget(StrongBodyLabel("Token:"), 1, 0)
        self.token_edit = PasswordLineEdit()
        self.token_edit.setText(DEFAULT_ADMIN_TOKEN)
        conn_layout.addWidget(self.token_edit, 1, 1)
        
        self.connect_btn = PrimaryPushButton(FluentIcon.LINK, "连接 / 刷新")
        self.connect_btn.clicked.connect(self.init_connection)
        conn_layout.addWidget(self.connect_btn, 2, 0, 1, 2)
        
        layout.addWidget(conn_card)
        layout.addStretch(1)

    # Legacy setup wrappers
    def setup_manage_tab_legacy(self, widget):
        self.manage_tab = widget # Map legacy self.manage_tab to new widget
        self.setup_manage_tab() # Call original method

    def setup_release_tab_legacy(self, widget):
        self.release_tab = widget
        self.setup_release_tab()

    def setup_deploy_tab_legacy(self, widget):
        self.deploy_tab = widget
        self.setup_deploy_tab()

    # Overwrite init_connection to update config interface client
    # (Merged into the main definition below)


    def setup_manage_tab(self):
        layout = QHBoxLayout(self.manage_tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Left Panel: Group List
        left_panel = SimpleCardWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(SubtitleLabel("用户组列表"))
        
        self.group_list_widget = ListWidget()
        self.group_list_widget.currentItemChanged.connect(self.on_group_selected)
        left_layout.addWidget(self.group_list_widget)
        
        self.add_group_btn = PrimaryPushButton(FluentIcon.ADD, "新建组")
        self.add_group_btn.clicked.connect(self.create_group)
        left_layout.addWidget(self.add_group_btn)
        
        layout.addWidget(left_panel, 1)
        
        # Right Panel: Group Details & Users
        # We can use a scroll area for right panel if content is long, but VBox is fine for now
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        
        # Group Details Header (Card)
        info_card = SimpleCardWidget()
        info_layout = QGridLayout(info_card)
        
        info_layout.addWidget(StrongBodyLabel("组信息"), 0, 0, 1, 3)
        
        self.lbl_group_name = BodyLabel("-")
        self.lbl_group_version = BodyLabel("-")
        self.lbl_group_comment = BodyLabel("-")
        
        self.btn_edit_comment = PushButton(FluentIcon.EDIT, "修改备注")
        self.btn_edit_comment.clicked.connect(self.edit_group_comment)
        
        info_layout.addWidget(BodyLabel("名称:"), 1, 0)
        info_layout.addWidget(self.lbl_group_name, 1, 1)
        
        info_layout.addWidget(BodyLabel("当前版本:"), 2, 0)
        info_layout.addWidget(self.lbl_group_version, 2, 1)
        
        info_layout.addWidget(BodyLabel("备注:"), 3, 0)
        info_layout.addWidget(self.lbl_group_comment, 3, 1)
        info_layout.addWidget(self.btn_edit_comment, 3, 2)
        
        right_layout.addWidget(info_card)
        
        # User List
        user_card = SimpleCardWidget()
        user_layout = QVBoxLayout(user_card)
        user_layout.addWidget(StrongBodyLabel("组内用户"))
        
        self.user_table = TableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["ID", "用户名", "权限", "操作"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.verticalHeader().hide()
        self.user_table.setSelectionBehavior(TableWidget.SelectRows)
        user_layout.addWidget(self.user_table)
        
        # Batch Actions
        action_layout = QHBoxLayout()
        self.btn_move_user = PushButton(FluentIcon.MOVE, "移动用户到其他组...")
        self.btn_move_user.clicked.connect(self.move_selected_user)
        self.btn_change_perm = PushButton(FluentIcon.PEOPLE, "修改用户权限...")
        self.btn_change_perm.clicked.connect(self.change_user_perm)
        
        action_layout.addWidget(self.btn_move_user)
        action_layout.addWidget(self.btn_change_perm)
        action_layout.addStretch()
        user_layout.addLayout(action_layout)
        
        right_layout.addWidget(user_card, 1) # Give it stretch factor
        
        layout.addWidget(right_panel, 3)

    def setup_release_tab(self):
        layout = QVBoxLayout(self.release_tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Section 1: Upload
        upload_card = HeaderCardWidget("1. 上传新版本 (ZIP)")
        # HeaderCardWidget 本身是一个 Frame，我们可以给它设置布局来放内容
        # 但标准的用法是它的 content 部分。
        # 这里为了简单，我们使用 SimpleCardWidget 并自己加 Title
        
        # 修正：使用自定义 Card 结构以获得最佳控制
        
        # 1. Upload Card
        upload_card = SimpleCardWidget()
        upload_layout = QVBoxLayout(upload_card)
        upload_layout.addWidget(StrongBodyLabel("1. 上传新版本 (ZIP)"))
        
        upload_content = QHBoxLayout()
        self.file_path_edit = LineEdit()
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setPlaceholderText("选择文件或文件夹...")
        
        self.browse_btn = PushButton(FluentIcon.FOLDER, "浏览...")
        self.browse_btn.clicked.connect(self.browse_file)
        
        self.upload_btn = PrimaryPushButton(FluentIcon.UP, "上传")
        self.upload_btn.clicked.connect(self.upload_file)
        
        upload_content.addWidget(self.file_path_edit)
        upload_content.addWidget(self.browse_btn)
        upload_content.addWidget(self.upload_btn)
        
        upload_layout.addLayout(upload_content)
        layout.addWidget(upload_card)
        
        # Section 2: Archives List (New)
        archives_card = SimpleCardWidget()
        archives_layout = QVBoxLayout(archives_card)
        archives_layout.addWidget(StrongBodyLabel("2. 历史版本列表"))
        
        self.archives_list_widget = ListWidget()
        self.archives_list_widget.currentItemChanged.connect(self.on_archive_selected)
        archives_layout.addWidget(self.archives_list_widget)
        
        layout.addWidget(archives_card, 1) # Expand vertically

        # Section 3: Assign
        assign_card = SimpleCardWidget()
        assign_layout = QVBoxLayout(assign_card)
        assign_layout.addWidget(StrongBodyLabel("3. 分配版本给用户组"))
        
        assign_form = QGridLayout()
        assign_form.setSpacing(15)
        
        self.uploaded_filename_label = BodyLabel("无")
        self.uploaded_filename_label.setStyleSheet("font-weight: bold; color: #009FAA;")
        
        self.target_group_combo = ComboBox()
        self.assign_btn = PrimaryPushButton(FluentIcon.SYNC, "更新组版本")
        self.assign_btn.clicked.connect(self.assign_version)
        
        assign_form.addWidget(BodyLabel("选中版本:"), 0, 0)
        assign_form.addWidget(self.uploaded_filename_label, 0, 1)
        
        assign_form.addWidget(BodyLabel("目标组:"), 1, 0)
        assign_form.addWidget(self.target_group_combo, 1, 1)
        
        assign_form.addWidget(self.assign_btn, 2, 0, 1, 2)
        
        assign_layout.addLayout(assign_form)
        layout.addWidget(assign_card)
    
    def setup_deploy_tab(self):
        # Create a ScrollArea for deploy tab because content is tall
        scroll = ScrollArea()
        scroll.setWidgetResizable(True)
        self.deploy_tab.setLayout(QVBoxLayout())
        self.deploy_tab.layout().addWidget(scroll)
        
        container = QWidget()
        scroll.setWidget(container)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # ========== 区域 1: 服务器配置 ==========
        server_card = SimpleCardWidget()
        server_layout = QGridLayout(server_card)
        server_layout.setContentsMargins(20, 20, 20, 20)
        server_layout.setSpacing(15)
        
        server_layout.addWidget(StrongBodyLabel("服务器配置"), 0, 0, 1, 4)
        
        server_layout.addWidget(BodyLabel("服务器地址:"), 1, 0)
        self.deploy_host = LineEdit()
        self.deploy_host.setText("103.97.201.136")
        server_layout.addWidget(self.deploy_host, 1, 1)
        
        server_layout.addWidget(BodyLabel("SSH 端口:"), 1, 2)
        self.deploy_port = LineEdit()
        self.deploy_port.setText("22")
        server_layout.addWidget(self.deploy_port, 1, 3)
        
        server_layout.addWidget(BodyLabel("用户名:"), 2, 0)
        self.deploy_user = LineEdit()
        self.deploy_user.setText("root")
        server_layout.addWidget(self.deploy_user, 2, 1)
        
        server_layout.addWidget(BodyLabel("密码:"), 2, 2)
        self.deploy_password = PasswordLineEdit()
        server_layout.addWidget(self.deploy_password, 2, 3)
        
        btn_layout = QHBoxLayout()
        btn_test_conn = PushButton(FluentIcon.LINK, "测试连接")
        btn_test_conn.clicked.connect(self.test_ssh_connection)
        btn_layout.addWidget(btn_test_conn)
        
        btn_save_config = PushButton(FluentIcon.SAVE, "保存配置")
        btn_save_config.clicked.connect(self.save_deploy_config)
        btn_layout.addWidget(btn_save_config)
        
        btn_load_config = PushButton(FluentIcon.SYNC, "加载配置")
        btn_load_config.clicked.connect(self.load_deploy_config)
        btn_layout.addWidget(btn_load_config)
        
        server_layout.addLayout(btn_layout, 3, 0, 1, 4)
        
        layout.addWidget(server_card)
        
        # ========== 区域 1.5: 后端服务自动化部署 ==========
        backend_card = SimpleCardWidget()
        backend_layout = QGridLayout(backend_card)
        backend_layout.setContentsMargins(20, 20, 20, 20)
        backend_layout.setSpacing(15)
        
        backend_layout.addWidget(StrongBodyLabel("🔧 后端服务自动化部署"), 0, 0, 1, 3)
        
        # 本地Server目录选择
        backend_layout.addWidget(BodyLabel("Server 目录:"), 1, 0)
        self.backend_server_path = LineEdit()
        self.backend_server_path.setPlaceholderText("选择本地 Server 目录（包含后端代码）")
        backend_layout.addWidget(self.backend_server_path, 1, 1)
        
        btn_browse_server = PushButton(FluentIcon.FOLDER, "浏览...")
        btn_browse_server.clicked.connect(self.browse_server_dir)
        backend_layout.addWidget(btn_browse_server, 1, 2)
        
        # 操作按钮行1：完整部署
        self.btn_full_deploy_backend = PrimaryPushButton(FluentIcon.SEND, "🚀 完整部署（上传+重启）")
        self.btn_full_deploy_backend.clicked.connect(self.full_deploy_backend)
        self.btn_full_deploy_backend.setToolTip("上传Server目录并重启Docker服务")
        backend_layout.addWidget(self.btn_full_deploy_backend, 2, 0, 1, 3)
        
        # 操作按钮行2：快捷操作
        btn_layout2 = QHBoxLayout()
        
        self.btn_restart_backend = PushButton(FluentIcon.SYNC, "仅重启服务")
        self.btn_restart_backend.clicked.connect(self.restart_backend_service)
        self.btn_restart_backend.setToolTip("仅重启Docker容器（不上传代码）")
        btn_layout2.addWidget(self.btn_restart_backend)
        
        self.btn_rebuild_backend = PushButton(FluentIcon.CONSTRACT, "重新构建")
        self.btn_rebuild_backend.clicked.connect(self.rebuild_and_deploy_backend)
        self.btn_rebuild_backend.setToolTip("重新构建Docker镜像")
        btn_layout2.addWidget(self.btn_rebuild_backend)
        
        self.btn_check_backend = PushButton(FluentIcon.SEARCH, "检查状态")
        self.btn_check_backend.clicked.connect(self.check_backend_status)
        btn_layout2.addWidget(self.btn_check_backend)

        self.btn_sync_db = PushButton(FluentIcon.SYNC, "同步数据库")
        self.btn_sync_db.clicked.connect(self.sync_database_schema)
        self.btn_sync_db.setToolTip("在服务器执行数据库结构同步脚本")
        btn_layout2.addWidget(self.btn_sync_db)
        
        backend_layout.addLayout(btn_layout2, 3, 0, 1, 3)
        
        layout.addWidget(backend_card)
        
        # ========== 区域 1.8: 后端版本历史 ==========
        backend_history_card = SimpleCardWidget()
        backend_history_layout = QVBoxLayout(backend_history_card)
        backend_history_layout.addWidget(StrongBodyLabel("📚 后端部署历史"))
        
        # 版本列表
        self.backend_version_table = TableWidget()
        self.backend_version_table.setColumnCount(5)
        self.backend_version_table.setHorizontalHeaderLabels(["版本号", "部署时间", "大小(MB)", "备注", "状态"])
        self.backend_version_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.backend_version_table.verticalHeader().hide()
        self.backend_version_table.setSelectionBehavior(TableWidget.SelectRows)
        self.backend_version_table.setMaximumHeight(200)
        backend_history_layout.addWidget(self.backend_version_table)
        
        # 操作按钮
        backend_btn_layout = QHBoxLayout()
        
        self.btn_refresh_backend_versions = PushButton(FluentIcon.SYNC, "刷新列表")
        self.btn_refresh_backend_versions.clicked.connect(self.refresh_backend_version_list)
        backend_btn_layout.addWidget(self.btn_refresh_backend_versions)
        
        self.btn_detect_backend_current = PushButton(FluentIcon.SEARCH, "检测当前版本")
        self.btn_detect_backend_current.clicked.connect(self.detect_backend_current_version)
        backend_btn_layout.addWidget(self.btn_detect_backend_current)
        
        self.btn_rollback_backend = PushButton(FluentIcon.HISTORY, "回滚到选中版本")
        self.btn_rollback_backend.clicked.connect(self.rollback_backend_version)
        backend_btn_layout.addWidget(self.btn_rollback_backend)
        
        self.btn_delete_backend_version = PushButton(FluentIcon.DELETE, "删除选中版本")
        self.btn_delete_backend_version.clicked.connect(self.delete_backend_version)
        backend_btn_layout.addWidget(self.btn_delete_backend_version)
        
        backend_btn_layout.addStretch()
        backend_history_layout.addLayout(backend_btn_layout)
        
        layout.addWidget(backend_history_card)
        
        # ========== 区域 2: 前端部署新版本 ==========
        layout.addWidget(StrongBodyLabel("🎨 前端应用部署"))
        deploy_new_card = SimpleCardWidget()
        deploy_new_layout = QGridLayout(deploy_new_card)
        deploy_new_layout.setContentsMargins(20, 20, 20, 20)
        deploy_new_layout.setSpacing(15)
        
        deploy_new_layout.addWidget(StrongBodyLabel("📦 部署新版本"), 0, 0, 1, 3)
        
        deploy_new_layout.addWidget(BodyLabel("dist_core 目录:"), 1, 0)
        self.dist_core_path = LineEdit()
        self.dist_core_path.setPlaceholderText("请选择已构建好的 dist_core 目录")
        deploy_new_layout.addWidget(self.dist_core_path, 1, 1)
        
        btn_browse_dist = PushButton(FluentIcon.FOLDER, "浏览...")
        btn_browse_dist.clicked.connect(self.browse_dist_core)
        deploy_new_layout.addWidget(btn_browse_dist, 1, 2)
        
        deploy_new_layout.addWidget(BodyLabel("备注（可选）:"), 2, 0)
        self.deploy_comment = LineEdit()
        self.deploy_comment.setPlaceholderText("例如: 修复主题同步bug")
        deploy_new_layout.addWidget(self.deploy_comment, 2, 1, 1, 2)
        
        self.btn_deploy_now = PrimaryPushButton(FluentIcon.SEND, "🚀 部署到服务器")
        # self.btn_deploy_now.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.btn_deploy_now.clicked.connect(self.deploy_new_version)
        deploy_new_layout.addWidget(self.btn_deploy_now, 3, 0, 1, 3)
        
        layout.addWidget(deploy_new_card)
        
        # ========== 区域 3: 版本历史管理 ==========
        history_card = SimpleCardWidget()
        history_layout = QVBoxLayout(history_card)
        history_layout.addWidget(StrongBodyLabel("📚 版本历史管理"))
        
        # 版本列表
        self.version_table = TableWidget()
        self.version_table.setColumnCount(5)
        self.version_table.setHorizontalHeaderLabels(["版本号", "部署时间", "大小(MB)", "备注", "状态"])
        self.version_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.version_table.verticalHeader().hide()
        self.version_table.setSelectionBehavior(TableWidget.SelectRows)
        history_layout.addWidget(self.version_table)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        
        self.btn_refresh_versions = PushButton(FluentIcon.SYNC, "刷新列表")
        self.btn_refresh_versions.clicked.connect(self.refresh_version_list)
        btn_layout.addWidget(self.btn_refresh_versions)
        
        self.btn_detect_current = PushButton(FluentIcon.SEARCH, "检测当前版本")
        self.btn_detect_current.clicked.connect(self.detect_current_version)
        # self.btn_detect_current.setStyleSheet("background-color: #2196F3; color: white;")
        btn_layout.addWidget(self.btn_detect_current)
        
        self.btn_rollback = PushButton(FluentIcon.HISTORY, "回滚到选中版本")
        self.btn_rollback.clicked.connect(self.rollback_version)
        btn_layout.addWidget(self.btn_rollback)
        
        self.btn_delete_version = PushButton(FluentIcon.DELETE, "删除选中版本")
        self.btn_delete_version.clicked.connect(self.delete_version)
        btn_layout.addWidget(self.btn_delete_version)
        
        btn_layout.addStretch()
        history_layout.addLayout(btn_layout)
        
        layout.addWidget(history_card)
        
        # ========== 区域 4: 部署日志 ==========
        layout.addWidget(StrongBodyLabel("部署日志:"))
        
        self.deploy_log = TextEdit() # Fluent TextEdit
        self.deploy_log.setReadOnly(True)
        # self.deploy_log.setStyleSheet("background-color: #1E1E1E; color: #D4D4D4; font-family: Consolas, monospace;")
        self.deploy_log.setMaximumHeight(200)
        layout.addWidget(self.deploy_log)
        
        # 加载配置和版本列表
        self.load_deploy_config()
        self.refresh_version_list()
        self.refresh_backend_version_list()

    def init_connection(self):
        url = self.url_edit.text()
        token = self.token_edit.text()
        self.api_client = ApiClient(url, token)
        
        try:
            self.refresh_all_data()
            
            # Sync client to config interface
            if hasattr(self, 'config_interface'):
                self.config_interface.api_client = self.api_client
            
            # self.tabs.setEnabled(True) # Legacy
            InfoBar.success("连接成功", "已成功连接到服务器", parent=self)
        except Exception as e:
            # 只显示警告，不阻止使用
            error_msg = str(e)
            if "500" in error_msg or "groups" in error_msg.lower():
                InfoBar.warning(
                    "部分功能不可用", 
                    f"组与用户管理功能暂时不可用：{e}\n这不影响「自动化部署」功能的使用。",
                    duration=5000,
                    parent=self
                )
            else:
                InfoBar.error("连接错误", str(e), parent=self)

    def refresh_all_data(self):
        if not self.api_client: return
        try:
            self.groups_data = self.api_client.list_groups()
            self.users_data = self.api_client.list_users()
            self.archives_data = self.api_client.list_archives()
            self.update_ui_with_data()
        except Exception as e:
            # 改为警告提示，不阻止使用
            error_msg = str(e)
            if "groups" in error_msg.lower():
                InfoBar.warning("警告", "组管理功能暂时不可用，但部署功能正常", parent=self)
            else:
                InfoBar.warning("警告", f"部分数据加载失败: {e}", parent=self)

    def update_ui_with_data(self):
        # Update Group List
        self.group_list_widget.clear()
        self.target_group_combo.clear()
        
        # 1. Add "Unassigned" pseudo-group
        unassigned_group = {
            'id': None,
            'name': '未分配组 (Unassigned)',
            'current_version_file': '-',
            'comment': '新注册或未分配的用户'
        }
        item_unassigned = QListWidgetItem(unassigned_group['name'])
        item_unassigned.setData(Qt.UserRole, unassigned_group)
        self.group_list_widget.addItem(item_unassigned)

        # 2. Add real groups
        for g in self.groups_data:
            item = QListWidgetItem(g['name'])
            item.setData(Qt.UserRole, g)
            self.group_list_widget.addItem(item)
            
            # Update Combo in Release Tab
            self.target_group_combo.addItem(g['name'], g['id'])
            
        # If there's a selection, refresh the user view, otherwise select first
        if self.group_list_widget.count() > 0:
             self.group_list_widget.setCurrentRow(0)

        # Update Archives List
        self.archives_list_widget.clear()
        for filename in self.archives_data:
            self.archives_list_widget.addItem(filename)

    def on_group_selected(self, current, previous):
        if not current: return
        group = current.data(Qt.UserRole)
        
        # Update Header
        self.lbl_group_name.setText(group['name'])
        self.lbl_group_version.setText(group['current_version_file'] or "无")
        self.lbl_group_comment.setText(group['comment'] or "无")
        
        # Filter Users
        if group['id'] is None:
            # Special handling for unassigned users
            group_users = [u for u in self.users_data if u['group_id'] is None]
        else:
            group_users = [u for u in self.users_data if u['group_id'] == group['id']]
            
        self.user_table.setRowCount(len(group_users))
        
        for i, u in enumerate(group_users):
            self.user_table.setItem(i, 0, QTableWidgetItem(str(u['id'])))
            self.user_table.setItem(i, 1, QTableWidgetItem(u['username']))
            self.user_table.setItem(i, 2, QTableWidgetItem(u['permissions'] or ""))
            # Store user object in first item
            self.user_table.item(i, 0).setData(Qt.UserRole, u)

    def on_archive_selected(self, current, previous):
        if not current: return
        filename = current.text()
        self.uploaded_filename_label.setText(filename)

    def create_group(self):
        dialog = CreateGroupDialog(self)
        if dialog.exec():
            name, comment = dialog.get_data()
            if not name:
                InfoBar.warning("警告", "组名称必填", parent=self)
                return
            try:
                self.api_client.create_group(name, comment)
                self.refresh_all_data()
                InfoBar.success("成功", f"组 '{name}' 创建成功!", parent=self)
            except Exception as e:
                InfoBar.error("错误", str(e), parent=self)

    def edit_group_comment(self):
        item = self.group_list_widget.currentItem()
        if not item: return
        group = item.data(Qt.UserRole)
        
        dialog = SimpleInputDialog("修改备注", "请输入新备注:", group['comment'] or "", self)
        if dialog.exec():
            text = dialog.get_text()
            try:
                self.api_client.update_group_comment(group['id'], text)
                self.refresh_all_data()
            except Exception as e:
                InfoBar.error("错误", str(e), parent=self)

    def move_selected_user(self):
        row = self.user_table.currentRow()
        if row < 0:
            InfoBar.warning("警告", "请先在列表中选择一个用户", parent=self)
            return
            
        user = self.user_table.item(row, 0).data(Qt.UserRole)
        
        # Create a simple dialog with combo box
        dialog = MessageBoxBase(self)
        dialog.titleLabel.setText("移动用户")
        
        combo = ComboBox()
        for g in self.groups_data:
            if g['id'] != user['group_id']:
                combo.addItem(g['name'], g['id'])
                
        dialog.viewLayout.addWidget(BodyLabel(f"将用户 {user['username']} 移动到:"))
        dialog.viewLayout.addWidget(combo)
        dialog.yesButton.setText("确定")
        dialog.cancelButton.setText("取消")
        
        if dialog.exec():
            new_group_id = combo.currentData()
            if new_group_id:
                try:
                    self.api_client.update_user_group(user['id'], new_group_id)
                    self.refresh_all_data()
                    InfoBar.success("成功", "用户移动成功", parent=self)
                except Exception as e:
                    InfoBar.error("错误", str(e), parent=self)

    def change_user_perm(self):
        row = self.user_table.currentRow()
        if row < 0:
            InfoBar.warning("警告", "请先在列表中选择一个用户", parent=self)
            return
        
        user = self.user_table.item(row, 0).data(Qt.UserRole)
        
        dialog = SimpleInputDialog("修改权限", "输入权限 (逗号分隔):", user['permissions'] or "", self)
        if dialog.exec():
            text = dialog.get_text()
            try:
                self.api_client.update_user_permissions(user['id'], text)
                self.refresh_all_data()
            except Exception as e:
                InfoBar.error("错误", str(e), parent=self)

    def browse_file(self):
        path = QFileDialog.getExistingDirectory(self, "选择发布文件夹 (自动压缩)")
        if path:
            self.file_path_edit.setText(path)

    def upload_file(self):
        path = self.file_path_edit.text()
        if not path or not os.path.exists(path):
            InfoBar.warning("警告", "请先选择有效的路径。", parent=self)
            return
        
        try:
            self.upload_btn.setEnabled(False)
            self.upload_btn.setText("处理中...")
            QApplication.processEvents()
            
            final_file_path = path
            
            # If directory, zip it first
            if os.path.isdir(path):
                self.upload_btn.setText("正在压缩...")
                QApplication.processEvents()
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_name = os.path.basename(os.path.abspath(path))
                zip_filename = f"{base_name}_{timestamp}.zip"
                
                def zip_directory(source_dir, output_filename):
                    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(source_dir):
                            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'dist', 'archives', '__pycache__']]
                            for file in files:
                                if file == output_filename or file.endswith('.zip') or file.endswith('.pyc'):
                                    continue
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, source_dir)
                                zipf.write(file_path, arcname)
                
                zip_directory(path, zip_filename)
                final_file_path = zip_filename
                
            self.upload_btn.setText("正在上传...")
            QApplication.processEvents()
            
            filename = self.api_client.upload_version(final_file_path)
            
            InfoBar.success("成功", f"上传成功: {filename}", parent=self)
            self.refresh_all_data()
        except Exception as e:
            InfoBar.error("上传错误", str(e), parent=self)
        finally:
            self.upload_btn.setEnabled(True)
            self.upload_btn.setText("上传")

    def assign_version(self):
        filename = self.uploaded_filename_label.text()
        if filename == "无" or not filename:
            InfoBar.warning("警告", "请先上传文件。", parent=self)
            return
        
        group_id = self.target_group_combo.currentData()
        if group_id is None:
            InfoBar.warning("警告", "请选择目标组。", parent=self)
            return
            
        try:
            self.api_client.update_group_version(group_id, filename)
            self.refresh_all_data()
            InfoBar.success("成功", f"组版本已更新为 {filename}", parent=self)
        except Exception as e:
            InfoBar.error("错误", str(e), parent=self)
    
    # ==================== 部署相关方法 ====================
    
    def browse_dist_core(self):
        """浏览选择 dist_core 目录"""
        path = QFileDialog.getExistingDirectory(self, "选择 dist_core 目录")
        if path:
            self.dist_core_path.setText(path)
    
    def refresh_version_list(self):
        """刷新版本历史列表"""
        try:
            # 首次调用时初始化数据库
            if not self.db_initialized:
                try:
                    self.db_manager.init_table()
                    self.db_initialized = True
                    self.log_deploy("✅ 版本管理系统连接成功")
                except Exception as e:
                    self.log_deploy(f"❌ 版本系统连接失败: {e}")
                    self.log_deploy("⚠️ 部署功能需要 SSH 支持，请检查配置")
                    return
            
            deployments = self.db_manager.get_all_deployments()
            self.version_table.setRowCount(len(deployments))
            
            for i, dep in enumerate(deployments):
                self.version_table.setItem(i, 0, QTableWidgetItem(dep['version']))
                self.version_table.setItem(i, 1, QTableWidgetItem(str(dep['deployed_at'])))
                self.version_table.setItem(i, 2, QTableWidgetItem(str(dep.get('file_size_mb', '-'))))
                self.version_table.setItem(i, 3, QTableWidgetItem(dep.get('comment', '') or ''))
                
                status_item = QTableWidgetItem("✅ 当前" if dep.get('is_current') else "")
                if dep.get('is_current'):
                    status_item.setForeground(Qt.green)
                self.version_table.setItem(i, 4, status_item)
                
                # 存储完整数据
                self.version_table.item(i, 0).setData(Qt.UserRole, dep)
            
            if len(deployments) == 0:
                self.log_deploy("ℹ️ 暂无版本记录，点击「🔍 检测当前版本」扫描服务器")
            else:
                self.log_deploy(f"✅ 已加载 {len(deployments)} 个历史版本")
        except Exception as e:
            self.log_deploy(f"❌ 加载版本列表失败: {e}")
    
    def detect_current_version(self):
        """检测服务器当前部署的版本"""
        if not self.deploy_host.text() or not self.deploy_user.text():
            InfoBar.warning("配置不完整", "请先配置服务器信息", parent=self)
            return
        
        w = MessageBox(
            '检测当前版本',
            "即将扫描服务器 /var/www/app/ 目录\n"
            "并将其注册为一个版本记录。\n\n"
            "是否继续？",
            self
        )
        
        if not w.exec():
            return
        
        self.deploy_log.clear()
        self.log_deploy("="*60)
        self.log_deploy("🔍 检测服务器当前版本")
        self.log_deploy("="*60)
        
        try:
            # 连接 SSH
            self.log_deploy("\n🔐 连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
            
            # 检查 /var/www/app 是否存在且不为空
            self.log_deploy("\n📁 检查 /var/www/app/ 目录...")
            stdin, stdout, stderr = ssh.exec_command('ls -A /var/www/app/ 2>/dev/null | wc -l')
            file_count = int(stdout.read().decode().strip())
            
            if file_count == 0:
                self.log_deploy("  目录为空或不存在")
                MessageBox("检测结果", "服务器 /var/www/app/ 目录为空\n无当前版本", self).exec()
                ssh.close()
                return
            
            self.log_deploy(f"  ✅ 检测到 {file_count} 个文件/目录")
            
            # 计算文件大小
            self.log_deploy("\n📊 计算文件大小...")
            stdin, stdout, stderr = ssh.exec_command('du -sm /var/www/app/ | cut -f1')
            size_mb = float(stdout.read().decode().strip())
            self.log_deploy(f"  大小: {size_mb} MB")
            
            # 获取最后修改时间
            stdin, stdout, stderr = ssh.exec_command(
                'find /var/www/app/ -type f -exec stat -c %Y {} \\; 2>/dev/null | sort -n | tail -1'
            )
            last_modified_timestamp = stdout.read().decode().strip()
            
            if last_modified_timestamp:
                from datetime import datetime
                last_modified = datetime.fromtimestamp(int(last_modified_timestamp))
                version = f"existing_{last_modified.strftime('%Y%m%d_%H%M%S')}"
            else:
                version = f"existing_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.log_deploy(f"\n📝 创建版本记录: {version}")
            
            # 备份当前版本到 app_versions
            self.log_deploy("\n💾 备份到版本历史...")
            ssh.exec_command(f'mkdir -p /var/www/app_versions/{version}')
            stdin, stdout, stderr = ssh.exec_command(
                f'cp -r /var/www/app/* /var/www/app_versions/{version}/'
            )
            stdout.channel.recv_exit_status()
            self.log_deploy("  ✅ 备份完成")
            
            ssh.close()
            
            # 记录到版本系统
            self.log_deploy("\n💾 保存版本记录...")
            comment = f"检测到的现有版本（{datetime.now().strftime('%Y-%m-%d')}）"
            self.db_manager.add_deployment(version, size_mb, comment)
            self.log_deploy("  ✅ 版本记录已保存")
            
            # 刷新列表
            self.refresh_version_list()
            
            self.log_deploy("\n" + "="*60)
            self.log_deploy("✅ 检测完成！")
            self.log_deploy("="*60)
            self.log_deploy(f"\n版本: {version}")
            self.log_deploy(f"大小: {size_mb} MB")
            self.log_deploy(f"备注: {comment}")
            
            MessageBox(
                "检测成功", 
                f"已检测并记录当前版本：\n\n"
                f"版本号: {version}\n"
                f"大小: {size_mb} MB\n\n"
                f"该版本已备份到服务器版本历史中",
                self
            ).exec()
            
        except Exception as e:
            self.log_deploy(f"\n❌ 检测失败: {e}")
            InfoBar.error("检测失败", str(e), parent=self)
    
    def deploy_new_version(self):
        """部署新版本到服务器"""
        dist_core_path = self.dist_core_path.text()
        
        # 验证
        if not dist_core_path or not os.path.exists(dist_core_path):
            InfoBar.warning("路径错误", "请选择有效的 dist_core 目录", parent=self)
            return
        
        if not os.path.isdir(dist_core_path):
            InfoBar.warning("路径错误", "请选择目录而不是文件", parent=self)
            return
        
        if not self.deploy_host.text() or not self.deploy_user.text():
            InfoBar.warning("配置不完整", "请先配置服务器信息", parent=self)
            return
        
        # 确认部署
        w = MessageBox(
            '确认部署',
            f"即将部署到服务器: {self.deploy_host.text()}\n"
            f"目标路径: /var/www/app/\n\n"
            f"这将替换当前正在运行的版本！\n是否继续？",
            self
        )
        
        if not w.exec():
            return
        
        # 禁用按钮
        self.btn_deploy_now.setEnabled(False)
        self.deploy_log.clear()
        
        try:
            # 生成版本号（时间戳）
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
            comment = self.deploy_comment.text() or None
            
            self.log_deploy("="*60)
            self.log_deploy(f"🚀 开始部署新版本: {version}")
            self.log_deploy("="*60)
            
            # 计算文件大小
            total_size = 0
            for root, dirs, files in os.walk(dist_core_path):
                for file in files:
                    total_size += os.path.getsize(os.path.join(root, file))
            file_size_mb = round(total_size / (1024 * 1024), 2)
            self.log_deploy(f"📦 待上传文件大小: {file_size_mb} MB")
            
            # 连接 SSH
            self.log_deploy("\n🔐 连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
            
            # 备份当前版本
            self.log_deploy("\n💾 备份当前版本...")
            sftp = ssh.open_sftp()
            
            try:
                # 检查 /var/www/app 是否存在且不为空
                stdin, stdout, stderr = ssh.exec_command('ls -A /var/www/app/ 2>/dev/null | wc -l')
                file_count = int(stdout.read().decode().strip())
                
                if file_count > 0:
                    backup_version = f"backup_{version}"
                    self.log_deploy(f"  当前版本不为空，备份为: {backup_version}")
                    
                    # 创建备份目录
                    ssh.exec_command(f'mkdir -p /var/www/app_versions/{backup_version}')
                    
                    # 复制当前版本到备份
                    stdin, stdout, stderr = ssh.exec_command(
                        f'cp -r /var/www/app/* /var/www/app_versions/{backup_version}/'
                    )
                    stdout.channel.recv_exit_status()
                    self.log_deploy(f"  ✅ 备份完成")
                else:
                    self.log_deploy("  当前版本为空，跳过备份")
            except Exception as e:
                self.log_deploy(f"  ⚠️ 备份失败（可能是首次部署）: {e}")
            
            # 清空当前目录
            self.log_deploy("\n🗑️ 清空当前目录...")
            stdin, stdout, stderr = ssh.exec_command('rm -rf /var/www/app/*')
            stdout.channel.recv_exit_status()
            self.log_deploy("  ✅ 目录已清空")
            
            # 创建版本存档目录
            ssh.exec_command(f'mkdir -p /var/www/app_versions/{version}')
            
            # 上传新版本
            self.log_deploy("\n📤 上传新版本...")
            self._upload_directory_with_progress(sftp, dist_core_path, '/var/www/app')
            self.log_deploy("  ✅ 上传完成")
            
            # 同时保存到版本历史目录
            self.log_deploy("\n💾 保存到版本历史...")
            stdin, stdout, stderr = ssh.exec_command(
                f'cp -r /var/www/app/* /var/www/app_versions/{version}/'
            )
            stdout.channel.recv_exit_status()
            self.log_deploy("  ✅ 版本历史已保存")
            
            sftp.close()
            ssh.close()
            
            # 记录到数据库
            self.log_deploy("\n💾 更新数据库记录...")
            self.db_manager.add_deployment(version, file_size_mb, comment)
            self.log_deploy("  ✅ 数据库记录已更新")
            
            # 刷新版本列表
            self.refresh_version_list()
            
            self.log_deploy("\n" + "="*60)
            self.log_deploy("🎉 部署完成！")
            self.log_deploy("="*60)
            self.log_deploy(f"\n访问地址: https://{self.deploy_host.text()}/")
            
            MessageBox("部署成功", f"版本 {version} 部署成功！", self).exec()
            
            # 清空输入
            self.dist_core_path.clear()
            self.deploy_comment.clear()
            
        except Exception as e:
            self.log_deploy(f"\n❌ 部署失败: {e}")
            InfoBar.error("部署失败", str(e), parent=self)
        finally:
            self.btn_deploy_now.setEnabled(True)
    
    def rollback_version(self):
        """回滚到选中的历史版本"""
        row = self.version_table.currentRow()
        if row < 0:
            InfoBar.warning("未选择版本", "请先选择要回滚的版本", parent=self)
            return
        
        dep = self.version_table.item(row, 0).data(Qt.UserRole)
        version = dep['version']
        
        if dep['is_current']:
            InfoBar.info("提示", "该版本已经是当前版本", parent=self)
            return
        
        # 确认回滚
        w = MessageBox(
            '确认回滚',
            f"即将回滚到版本: {version}\n"
            f"部署时间: {dep['deployed_at']}\n"
            f"备注: {dep['comment'] or '无'}\n\n"
            f"这将替换当前正在运行的版本！\n是否继续？",
            self
        )
        
        if not w.exec():
            return
        
        self.deploy_log.clear()
        self.log_deploy("="*60)
        self.log_deploy(f"⏪ 开始回滚到版本: {version}")
        self.log_deploy("="*60)
        
        try:
            # 连接 SSH
            self.log_deploy("\n🔐 连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
            
            # 备份当前版本
            self.log_deploy("\n💾 备份当前版本...")
            backup_version = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            ssh.exec_command(f'mkdir -p /var/www/app_versions/{backup_version}')
            stdin, stdout, stderr = ssh.exec_command(
                f'cp -r /var/www/app/* /var/www/app_versions/{backup_version}/'
            )
            stdout.channel.recv_exit_status()
            self.log_deploy(f"  ✅ 当前版本已备份为: {backup_version}")
            
            # 清空当前目录
            self.log_deploy("\n🗑️ 清空当前目录...")
            stdin, stdout, stderr = ssh.exec_command('rm -rf /var/www/app/*')
            stdout.channel.recv_exit_status()
            self.log_deploy("  ✅ 目录已清空")
            
            # 从历史版本复制
            self.log_deploy("\n📋 从历史版本复制...")
            stdin, stdout, stderr = ssh.exec_command(
                f'cp -r /var/www/app_versions/{version}/* /var/www/app/'
            )
            exit_code = stdout.channel.recv_exit_status()
            
            if exit_code != 0:
                error = stderr.read().decode()
                raise Exception(f"复制失败: {error}")
            
            self.log_deploy("  ✅ 版本复制完成")
            
            ssh.close()
            
            # 更新数据库
            self.log_deploy("\n💾 更新数据库记录...")
            self.db_manager.set_current_version(version)
            self.log_deploy("  ✅ 数据库已更新")
            
            # 刷新版本列表
            self.refresh_version_list()
            
            self.log_deploy("\n" + "="*60)
            self.log_deploy("🎉 回滚完成！")
            self.log_deploy("="*60)
            
            MessageBox("回滚成功", f"已成功回滚到版本 {version}", self).exec()
            
        except Exception as e:
            self.log_deploy(f"\n❌ 回滚失败: {e}")
            InfoBar.error("回滚失败", str(e), parent=self)
    
    def delete_version(self):
        """删除选中的版本"""
        row = self.version_table.currentRow()
        if row < 0:
            InfoBar.warning("未选择版本", "请先选择要删除的版本", parent=self)
            return
        
        dep = self.version_table.item(row, 0).data(Qt.UserRole)
        version = dep['version']
        
        if dep['is_current']:
            InfoBar.warning("无法删除", "不能删除当前正在使用的版本", parent=self)
            return
        
        # 确认删除
        w = MessageBox(
            '确认删除',
            f"确定要删除版本: {version}？\n\n"
            f"这将同时删除：\n"
            f"1. 数据库记录\n"
            f"2. 服务器上的版本文件 (/var/www/app_versions/{version}/)\n\n"
            f"此操作不可恢复！",
            self
        )
        
        if not w.exec():
            return
        
        try:
            # 连接 SSH 删除服务器文件
            self.log_deploy(f"\n🗑️ 删除版本: {version}")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            
            stdin, stdout, stderr = ssh.exec_command(f'rm -rf /var/www/app_versions/{version}')
            stdout.channel.recv_exit_status()
            ssh.close()
            
            self.log_deploy(f"  ✅ 服务器文件已删除")
            
            # 删除数据库记录
            self.db_manager.delete_deployment(version)
            self.log_deploy(f"  ✅ 数据库记录已删除")
            
            # 刷新列表
            self.refresh_version_list()
            
            MessageBox("删除成功", f"版本 {version} 已删除", self).exec()
            
        except Exception as e:
            self.log_deploy(f"  ❌ 删除失败: {e}")
            InfoBar.error("删除失败", str(e), parent=self)
    
    def _upload_directory_with_progress(self, sftp, local_dir, remote_dir):
        """递归上传目录（带进度提示）"""
        if not os.path.exists(local_dir):
            raise Exception(f"本地目录不存在: {local_dir}")
        
        # 创建远程目录
        try:
            sftp.stat(remote_dir)
        except IOError:
            sftp.mkdir(remote_dir)
        
        # 忽略列表
        IGNORED_DIRS = {'.git', '__pycache__', 'archives', 'venv', 'node_modules', '.idea', '.vscode'}
        IGNORED_FILES = {'.env', 'designercep.db', '.DS_Store', 'Thumbs.db'}
        
        # 递归上传文件
        for item in os.listdir(local_dir):
            # 检查忽略
            if item in IGNORED_DIRS or item in IGNORED_FILES:
                continue
            if item.endswith('.pyc') or item.endswith('.log') or item.endswith('.zip'):
                continue
                
            local_path = os.path.join(local_dir, item)
            remote_path = remote_dir + '/' + item
            
            if os.path.isfile(local_path):
                self.log_deploy(f"    → {item}")
                try:
                    sftp.put(local_path, remote_path)
                except Exception as e:
                    # 如果是 designercep.db 相关的临时文件或其他锁定文件，忽略错误
                    if "designercep.db" in item:
                        self.log_deploy(f"    ⚠️ 跳过锁定文件: {item}")
                        continue
                    raise e
                QApplication.processEvents()  # 保持 UI 响应
            elif os.path.isdir(local_path):
                self._upload_directory_with_progress(sftp, local_path, remote_path)
    
    def save_deploy_config(self):
        """保存部署配置到本地文件"""
        try:
            config_file = os.path.join(os.path.dirname(__file__), 'deploy_config.txt')
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(f"host={self.deploy_host.text()}\n")
                f.write(f"port={self.deploy_port.text()}\n")
                f.write(f"user={self.deploy_user.text()}\n")
                f.write(f"password={self.deploy_password.text()}\n")
            InfoBar.success("成功", "配置已保存", parent=self)
        except Exception as e:
            InfoBar.error("错误", f"保存配置失败: {e}", parent=self)

    def load_deploy_config(self):
        """从本地文件加载部署配置"""
        try:
            config_file = os.path.join(os.path.dirname(__file__), 'deploy_config.txt')
            if not os.path.exists(config_file):
                # 尝试从 deploy_config.json 加载
                json_config = os.path.join(os.path.dirname(__file__), 'deploy_config.json')
                if os.path.exists(json_config):
                    with open(json_config, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        self.deploy_host.setText(config.get('host', ''))
                        self.deploy_port.setText(str(config.get('port', '22')))
                        self.deploy_user.setText(config.get('username', ''))
                        self.deploy_password.setText(config.get('password', ''))
                return
            
            with open(config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if key == 'host':
                            self.deploy_host.setText(value)
                        elif key == 'port':
                            self.deploy_port.setText(value)
                        elif key == 'user':
                            self.deploy_user.setText(value)
                        elif key == 'password':
                            self.deploy_password.setText(value)
        except Exception as e:
            self.log_deploy(f"加载配置失败: {e}")

    def test_ssh_connection(self):
        """测试 SSH 连接"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            self.log_deploy("正在测试 SSH 连接...")
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=10
            )
            
            stdin, stdout, stderr = ssh.exec_command('pwd')
            remote_pwd = stdout.read().decode().strip()
            
            ssh.close()
            
            MessageBox("连接成功", f"SSH 连接测试成功！\n当前目录: {remote_pwd}", self).exec()
            self.log_deploy(f"✅ SSH 连接成功，当前目录: {remote_pwd}")
        except Exception as e:
            InfoBar.error("连接失败", f"SSH 连接测试失败:\n{str(e)}", parent=self)
            self.log_deploy(f"❌ SSH 连接失败: {e}")
    
    def log_deploy(self, message):
        """添加部署日志"""
        self.deploy_log.append(message)
        QApplication.processEvents()
    
    # ==================== 后端部署相关方法 ====================
    
    def browse_server_dir(self):
        """浏览选择 Server 目录"""
        path = QFileDialog.getExistingDirectory(self, "选择 Server 目录")
        if path:
            self.backend_server_path.setText(path)
    
    def full_deploy_backend(self):
        """完整部署后端：上传代码 + 重启服务"""
        server_path = self.backend_server_path.text()
        
        # 验证
        if not server_path or not os.path.exists(server_path):
            InfoBar.warning("路径错误", "请选择有效的 Server 目录", parent=self)
            return
        
        if not os.path.isdir(server_path):
            InfoBar.warning("路径错误", "请选择目录而不是文件", parent=self)
            return
        
        if not self.deploy_host.text() or not self.deploy_user.text():
            InfoBar.warning("配置不完整", "请先配置服务器信息", parent=self)
            return
        
        # 确认部署
        w = MessageBox(
            '确认完整部署',
            f"即将执行以下操作：\n"
            f"1. 上传 Server 目录到服务器\n"
            f"2. 重启 Docker 容器\n\n"
            f"本地目录: {server_path}\n"
            f"服务器: {self.deploy_host.text()}\n\n"
            f"是否继续？",
            self
        )
        
        if not w.exec():
            return
        
        # 禁用按钮
        self.btn_full_deploy_backend.setEnabled(False)
        self.deploy_log.clear()
        
        try:
            self.log_deploy("="*60)
            self.log_deploy("🚀 完整部署后端服务")
            self.log_deploy("="*60)
            
            # 连接 SSH
            self.log_deploy("\n🔐 连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
            
            # 打开 SFTP
            sftp = ssh.open_sftp()
            
            # 3. 备份旧目录
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_root = "/root/server_backups"
            ssh.exec_command(f'mkdir -p {backup_root}')
            
            backup_path = f'{backup_root}/Server_{timestamp}'
            
            stdin, stdout, stderr = ssh.exec_command(f'[ -d /root/Server ] && cp -r /root/Server {backup_path} || echo "首次部署"')
            output = stdout.read().decode().strip()
            if output == "首次部署":
                self.log_deploy("  ℹ️ 这是首次部署，无需备份")
            else:
                self.log_deploy(f"  ✅ 已备份到: {backup_path}")
            
            # 上传 Server 目录
            self.log_deploy("\n📤 上传 Server 目录...")
            self.log_deploy(f"  源路径: {server_path}")
            self.log_deploy(f"  目标路径: /root/server")
            
            # 确保目标目录存在
            stdin, stdout, stderr = ssh.exec_command('mkdir -p /root/Server')
            stdout.channel.recv_exit_status()
            
            # 删除旧文件（保留 .env 和数据）
            self.log_deploy("\n🗑️ 清理旧文件（保留配置）...")
            stdin, stdout, stderr = ssh.exec_command(
                'cd /root/Server && find . -mindepth 1 ! -name ".env" ! -name "designercep.db" ! -name "archives" -exec rm -rf {} + 2>/dev/null || true'
            )
            stdout.channel.recv_exit_status()
            
            # 上传新文件
            self.log_deploy("\n📁 上传文件...")
            self._upload_directory_with_progress(sftp, server_path, '/root/Server')
            self.log_deploy("  ✅ 上传完成")
            
            sftp.close()
            
            # 重启 Docker 服务
            self.log_deploy("\n🔄 重启 Docker 服务...")
            stdin, stdout, stderr = ssh.exec_command(
                'cd /root/Server && docker-compose restart backend'
            )
            
            # 实时输出日志
            for line in iter(stdout.readline, ""):
                if line.strip():
                    self.log_deploy(f"  {line.strip()}")
                    QApplication.processEvents()
            
            exit_code = stdout.channel.recv_exit_status()
            if exit_code != 0:
                error = stderr.read().decode()
                raise Exception(f"重启失败: {error}")
            
            self.log_deploy("  ✅ 服务重启成功")
            
            # 检查服务状态
            self.log_deploy("\n📊 检查服务状态...")
            import time
            time.sleep(3)
            
            stdin, stdout, stderr = ssh.exec_command(
                'cd /root/Server && docker-compose ps backend'
            )
            output = stdout.read().decode()
            self.log_deploy(output)
            
            # 健康检查
            self.log_deploy("\n🏥 健康检查...")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/health')
            health_output = stdout.read().decode()
            if health_output and 'healthy' in health_output.lower():
                self.log_deploy(f"  ✅ API 健康检查通过: {health_output}")
            else:
                self.log_deploy(f"  ⚠️ API 可能未就绪: {health_output}")
            
            ssh.close()
            
            # 记录版本到数据库
            self.log_deploy("\n💾 记录版本信息...")
            version = timestamp  # 使用时间戳作为版本号
            try:
                # 计算上传文件大小
                total_size = 0
                for root, dirs, files in os.walk(server_path):
                    for file in files:
                        total_size += os.path.getsize(os.path.join(root, file))
                file_size_mb = round(total_size / (1024 * 1024), 2)
                
                comment = "后端完整部署"
                self.backend_db_manager.add_deployment(version, file_size_mb, comment)
                self.log_deploy("  ✅ 版本记录已保存")
                
                # 刷新版本列表
                self.refresh_backend_version_list()
            except Exception as e:
                self.log_deploy(f"  ⚠️ 版本记录保存失败: {e}")
            
            self.log_deploy("\n" + "="*60)
            self.log_deploy("✅ 后端完整部署成功！")
            self.log_deploy("="*60)
            self.log_deploy(f"\n访问地址: https://{self.deploy_host.text()}/health")
            
            MessageBox("部署成功", "后端服务已完整部署并重启！", self).exec()
            
            # 清空输入
            self.backend_server_path.clear()
            
        except Exception as e:
            self.log_deploy(f"\n❌ 部署失败: {e}")
            InfoBar.error("部署失败", str(e), parent=self)
        finally:
            self.btn_full_deploy_backend.setEnabled(True)
    
    def restart_backend_service(self):
        """重启后端 Docker 服务"""
        if not self.deploy_host.text() or not self.deploy_user.text():
            InfoBar.warning("配置不完整", "请先配置服务器信息", parent=self)
            return
        
        w = MessageBox(
            '确认重启',
            "即将重启后端 Docker 服务\n"
            "这将导致服务短暂不可用（约10-30秒）\n\n"
            "是否继续？",
            self
        )
        
        if not w.exec():
            return
        
        self.deploy_log.clear()
        self.log_deploy("="*60)
        self.log_deploy("🔄 重启后端服务")
        self.log_deploy("="*60)
        
        try:
            self.log_deploy("\n🔐 连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
            
            # 进入 Server 目录
            self.log_deploy("\n📁 进入服务目录...")
            
            # 重启 docker-compose 服务
            self.log_deploy("\n🔄 重启 Docker 容器...")
            stdin, stdout, stderr = ssh.exec_command(
                'cd /root/Server && docker-compose restart backend'
            )
            exit_code = stdout.channel.recv_exit_status()
            
            if exit_code != 0:
                error = stderr.read().decode()
                raise Exception(f"重启失败: {error}")
            
            self.log_deploy("  ✅ 后端容器重启成功")
            
            # 等待服务启动
            self.log_deploy("\n⏳ 等待服务启动...")
            import time
            time.sleep(5)
            
            # 检查服务状态
            stdin, stdout, stderr = ssh.exec_command(
                'cd /root/Server && docker-compose ps backend'
            )
            output = stdout.read().decode()
            self.log_deploy(f"\n{output}")
            
            # 健康检查
            self.log_deploy("\n🏥 等待服务启动...")
            import time
            time.sleep(5)
            stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/health')
            health_output = stdout.read().decode()
            if health_output and 'healthy' in health_output.lower():
                self.log_deploy(f"  ✅ API 健康检查通过: {health_output}")
            else:
                self.log_deploy(f"  ⚠️ API 可能未就绪，请稍候再试")
            
            ssh.close()
            
            self.log_deploy("\n" + "="*60)
            self.log_deploy("✅ 后端服务重启完成！")
            self.log_deploy("="*60)
            
            MessageBox("重启成功", "后端服务已重启！", self).exec()
            
        except Exception as e:
            self.log_deploy(f"\n❌ 重启失败: {e}")
            InfoBar.error("重启失败", str(e), parent=self)
    
    def rebuild_and_deploy_backend(self):
        """重新构建并部署后端"""
        if not self.deploy_host.text() or not self.deploy_user.text():
            InfoBar.warning("配置不完整", "请先配置服务器信息", parent=self)
            return
        
        w = MessageBox(
            '确认重新构建',
            "即将重新构建并部署后端服务\n"
            "这个过程可能需要5-10分钟\n\n"
            "是否继续？",
            self
        )
        
        if not w.exec():
            return
        
        self.deploy_log.clear()
        self.log_deploy("="*60)
        self.log_deploy("🏗️ 重新构建并部署后端")
        self.log_deploy("="*60)
        
        try:
            self.log_deploy("\n🔐 连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
            
            # 1. 上传新代码到临时目录
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            remote_temp_dir = f"/root/Server_upload_{timestamp}"
            self.log_deploy(f"\n� 上传代码到临时目录: {remote_temp_dir}...")
            
            # 创建临时目录
            ssh.exec_command(f'mkdir -p {remote_temp_dir}')
            
            sftp = ssh.open_sftp()
            local_server_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Server')
            
            # 递归上传
            for root, dirs, files in os.walk(local_server_path):
                # 过滤不需要的目录
                dirs[:] = [d for d in dirs if d not in ['__pycache__', 'venv', '.git', '.idea', '.vscode', 'static']]
                
                rel_path = os.path.relpath(root, local_server_path)
                remote_root = os.path.join(remote_temp_dir, rel_path).replace('\\', '/')
                
                # 创建远程目录
                try:
                    sftp.stat(remote_root)
                except FileNotFoundError:
                    ssh.exec_command(f'mkdir -p {remote_root}')
                
                for file in files:
                    if file.endswith('.pyc') or file.endswith('.pyo'):
                        continue
                        
                    local_file = os.path.join(root, file)
                    remote_file = os.path.join(remote_root, file).replace('\\', '/')
                    
                    # self.log_deploy(f"  -> {file}")
                    sftp.put(local_file, remote_file)
            
            self.log_deploy("✅ 代码上传完成")
            
            # 2. 停止服务
            self.log_deploy("\n� 停止当前服务...")
            # 检查 /root/Server 是否存在
            stdin, stdout, stderr = ssh.exec_command('[ -d /root/Server ] && echo "exists" || echo "not found"')
            if stdout.read().decode().strip() == "exists":
                stdin, stdout, stderr = ssh.exec_command('cd /root/Server && docker-compose down')
                self.log_deploy(stdout.read().decode())
                
                # 3. 备份旧目录
                backup_root = "/root/server_backups"
                ssh.exec_command(f'mkdir -p {backup_root}')
                
                backup_dir = f"{backup_root}/Server_{timestamp}"
                self.log_deploy(f"📦 备份旧目录到: {backup_dir}")
                ssh.exec_command(f'mv /root/Server {backup_dir}')
                
                # 4. 迁移关键数据 (.env, archives, db)
                self.log_deploy("� 迁移配置文件和数据...")
                # 复制 .env
                ssh.exec_command(f'cp {backup_dir}/.env {remote_temp_dir}/.env 2>/dev/null')
                # 复制 archives (如果新目录没有)
                ssh.exec_command(f'[ ! -d {remote_temp_dir}/archives ] && cp -r {backup_dir}/archives {remote_temp_dir}/archives 2>/dev/null')
                # 复制 sqlite db (如果有)
                ssh.exec_command(f'cp {backup_dir}/*.db {remote_temp_dir}/ 2>/dev/null')
                # 复制 mysql.cnf (如果有)
                ssh.exec_command(f'cp {backup_dir}/mysql.cnf {remote_temp_dir}/mysql.cnf 2>/dev/null')
            else:
                self.log_deploy("ℹ️这是首次部署 (未找到旧目录)")

            # 5. 启用新目录
            self.log_deploy(f"✅ 启用新版本目录...")
            ssh.exec_command(f'mv {remote_temp_dir} /root/Server')
            
            # 6. 重新构建并启动
            self.log_deploy("\n🚀 重新构建并启动服务...")
            self.log_deploy("  这可能需要几分钟，请耐心等待...")
            
            # 赋予 start.sh 执行权限
            ssh.exec_command('chmod +x /root/Server/start.sh')
            
            stdin, stdout, stderr = ssh.exec_command(
                'cd /root/Server && docker-compose up -d --build'
            )
            
            # 实时读取输出
            while True:
                line = stdout.readline()
                if not line:
                    break
                self.log_deploy("  " + line.strip())
            
            error = stderr.read().decode()
            if error and "Building" not in error and "Creating" not in error: # docker-compose stderr often contains normal info
                 self.log_deploy(f"⚠️ 输出:\n{error}")
            
            ssh.close()
            
            self.log_deploy("\n" + "="*60)
            self.log_deploy("✅ 部署完成！")
            self.log_deploy("建议点击 [检查状态] 确认服务健康状况")
            self.log_deploy("="*60)
            
            InfoBar.success("成功", "后端服务已重新构建并部署", parent=self)
            
        except Exception as e:
            self.log_deploy(f"\n❌ 部署失败: {e}")
            InfoBar.error("部署失败", str(e), parent=self)
    
    def check_backend_status(self):
        """检查后端服务状态"""
        if not self.deploy_host.text() or not self.deploy_user.text():
            InfoBar.warning("配置不完整", "请先配置服务器信息", parent=self)
            return
        
        self.deploy_log.clear()
        self.log_deploy("="*60)
        self.log_deploy("🔍 检查后端服务状态")
        self.log_deploy("="*60)
        
        try:
            self.log_deploy("\n🔐 连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
            
            # 检查 Docker 服务状态
            self.log_deploy("\n📊 Docker 容器状态:")
            stdin, stdout, stderr = ssh.exec_command(
                'cd /root/Server && docker-compose ps'
            )
            output = stdout.read().decode()
            self.log_deploy(output)
            
            # 检查后端日志（最近20行）
            self.log_deploy("\n📜 后端最近日志:")
            stdin, stdout, stderr = ssh.exec_command(
                'cd /root/Server && docker-compose logs --tail=20 backend'
            )
            output = stdout.read().decode()
            self.log_deploy(output)
            
            # 测试 API 健康检查
            self.log_deploy("\n🏥 健康检查:")
            stdin, stdout, stderr = ssh.exec_command(
                'curl -s http://localhost:8000/health'
            )
            output = stdout.read().decode()
            if output:
                self.log_deploy(f"  API 响应: {output}")
                self.log_deploy("  ✅ 后端服务运行正常")
            else:
                self.log_deploy("  ⚠️ 后端服务可能未启动")
            
            ssh.close()
            
            self.log_deploy("\n" + "="*60)
            self.log_deploy("✅ 状态检查完成")
            self.log_deploy("="*60)
            
        except Exception as e:
            self.log_deploy(f"\n❌ 检查失败: {e}")
            InfoBar.error("检查失败", str(e), parent=self)
    
    def sync_database_schema(self):
        """同步数据库结构"""
        if not self.deploy_host.text() or not self.deploy_user.text():
            InfoBar.warning("配置不完整", "请先配置服务器信息", parent=self)
            return
        
        w = MessageBox(
            '同步数据库',
            "即将连接服务器并同步数据库表结构\n"
            "这会自动创建缺失的表和字段。\n\n"
            "是否继续？",
            self
        )
        
        if not w.exec():
            return
        
        self.deploy_log.clear()
        self.log_deploy("="*60)
        self.log_deploy("🔄 开始同步数据库结构")
        self.log_deploy("="*60)
        
        try:
            self.log_deploy("\n🔐 连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
            
            # 1. 确保 init_db.py 存在
            self.log_deploy("\n📤 检查/上传同步脚本...")
            sftp = ssh.open_sftp()
            local_init_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Server', 'init_db.py')
            remote_init_db = '/root/Server/init_db.py'
            
            if os.path.exists(local_init_db):
                sftp.put(local_init_db, remote_init_db)
                self.log_deploy(f"  ✅ 已上传 init_db.py")
            else:
                self.log_deploy(f"  ⚠️ 本地未找到 {local_init_db}，尝试直接运行容器内已有脚本")
            
            # 2. 执行同步命令
            self.log_deploy("\n🚀 执行数据库同步...")
            
            # 先将脚本复制到容器内
            self.log_deploy("  📋 复制脚本到容器...")
            stdin, stdout, stderr = ssh.exec_command('docker cp /root/Server/init_db.py designercep_backend:/app/init_db.py')
            stdout.channel.recv_exit_status() # 等待完成
            
            # 然后在容器内执行
            cmd = 'docker exec designercep_backend python init_db.py'
            self.log_deploy(f"  $ {cmd}")
            
            stdin, stdout, stderr = ssh.exec_command(cmd)
            
            # 实时读取输出
            while True:
                line = stdout.readline()
                if not line:
                    break
                self.log_deploy("  " + line.strip())
                
            error = stderr.read().decode()
            if error:
                self.log_deploy(f"⚠️ 错误输出:\n{error}")
            
            ssh.close()
            
            self.log_deploy("\n✅ 同步操作完成")
            InfoBar.success("成功", "数据库同步指令已执行", parent=self)
            
        except Exception as e:
            self.log_deploy(f"\n❌ 同步失败: {e}")
            InfoBar.error("失败", str(e), parent=self)

    # ==================== 后端版本管理方法 ====================
    
    def refresh_backend_version_list(self):
        """刷新后端版本历史列表"""
        try:
            # 首次调用时初始化数据库
            if not self.backend_db_initialized:
                try:
                    self.backend_db_manager.init_table()
                    self.backend_db_initialized = True
                    self.log_deploy("✅ 后端版本管理系统连接成功")
                except Exception as e:
                    self.log_deploy(f"ℹ️ 后端版本系统初始化: {e}")
                    return
            
            deployments = self.backend_db_manager.get_all_deployments()
            self.backend_version_table.setRowCount(len(deployments))
            
            for i, dep in enumerate(deployments):
                self.backend_version_table.setItem(i, 0, QTableWidgetItem(dep['version']))
                self.backend_version_table.setItem(i, 1, QTableWidgetItem(str(dep['deployed_at'])))
                self.backend_version_table.setItem(i, 2, QTableWidgetItem(str(dep.get('file_size_mb', '-'))))
                self.backend_version_table.setItem(i, 3, QTableWidgetItem(dep.get('comment', '') or ''))
                
                status_item = QTableWidgetItem("✅ 当前" if dep.get('is_current') else "")
                if dep.get('is_current'):
                    status_item.setForeground(Qt.green)
                self.backend_version_table.setItem(i, 4, status_item)
                
                # 存储完整数据
                self.backend_version_table.item(i, 0).setData(Qt.UserRole, dep)
            
            if len(deployments) > 0:
                self.log_deploy(f"✅ 已加载 {len(deployments)} 个后端版本")
        except Exception as e:
            self.log_deploy(f"ℹ️ 加载后端版本列表: {e}")
    
    def detect_backend_current_version(self):
        """检测服务器当前部署的后端版本"""
        if not self.deploy_host.text() or not self.deploy_user.text():
            InfoBar.warning("配置不完整", "请先配置服务器信息", parent=self)
            return
        
        w = MessageBox(
            '检测当前版本',
            "即将扫描服务器 /root/Server/ 目录\n"
            "并将其注册为一个版本记录。\n\n"
            "是否继续？",
            self
        )
        
        if not w.exec():
            return
        
        self.deploy_log.clear()
        self.log_deploy("="*60)
        self.log_deploy("🔍 检测后端当前版本")
        self.log_deploy("="*60)
        
        try:
            self.log_deploy("\n🔐 连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
            
            # 检查 /root/Server 是否存在
            self.log_deploy("\n📁 检查 /root/Server/ 目录...")
            stdin, stdout, stderr = ssh.exec_command('ls -A /root/Server/ 2>/dev/null | wc -l')
            file_count = int(stdout.read().decode().strip())
            
            if file_count == 0:
                self.log_deploy("  目录为空或不存在")
                MessageBox("检测结果", "服务器 /root/Server/ 目录为空\n无当前版本", self).exec()
                ssh.close()
                return
            
            self.log_deploy(f"  ✅ 检测到 {file_count} 个文件/目录")
            
            # 计算文件大小
            self.log_deploy("\n📊 计算文件大小...")
            stdin, stdout, stderr = ssh.exec_command('du -sm /root/Server/ | cut -f1')
            size_mb = float(stdout.read().decode().strip())
            self.log_deploy(f"  大小: {size_mb} MB")
            
            # 生成版本号
            version = f"existing_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.log_deploy(f"\n📝 创建版本记录: {version}")
            
            # 备份当前版本
            self.log_deploy("\n💾 备份到版本历史...")
            ssh.exec_command(f'mkdir -p /root/server_versions/{version}')
            stdin, stdout, stderr = ssh.exec_command(
                f'cp -r /root/Server/* /root/server_versions/{version}/'
            )
            stdout.channel.recv_exit_status()
            self.log_deploy("  ✅ 备份完成")
            
            ssh.close()
            
            # 记录到版本系统
            self.log_deploy("\n💾 保存版本记录...")
            comment = f"检测到的现有版本（{datetime.now().strftime('%Y-%m-%d')}）"
            self.backend_db_manager.add_deployment(version, size_mb, comment)
            self.log_deploy("  ✅ 版本记录已保存")
            
            # 刷新列表
            self.refresh_backend_version_list()
            
            self.log_deploy("\n" + "="*60)
            self.log_deploy("✅ 检测完成！")
            self.log_deploy("="*60)
            
            MessageBox("检测成功", f"已检测并记录当前版本：\n\n版本号: {version}\n大小: {size_mb} MB", self).exec()
            
        except Exception as e:
            self.log_deploy(f"\n❌ 检测失败: {e}")
            InfoBar.error("检测失败", str(e), parent=self)
    
    def rollback_backend_version(self):
        """回滚到选中的后端历史版本"""
        row = self.backend_version_table.currentRow()
        if row < 0:
            InfoBar.warning("未选择版本", "请先选择要回滚的版本", parent=self)
            return
        
        dep = self.backend_version_table.item(row, 0).data(Qt.UserRole)
        version = dep['version']
        
        if dep['is_current']:
            InfoBar.info("提示", "该版本已经是当前版本", parent=self)
            return
        
        w = MessageBox(
            '确认回滚',
            f"即将回滚到版本: {version}\n"
            f"部署时间: {dep['deployed_at']}\n"
            f"备注: {dep['comment'] or '无'}\n\n"
            f"这将替换当前正在运行的后端代码！\n是否继续？",
            self
        )
        
        if not w.exec():
            return
        
        self.deploy_log.clear()
        self.log_deploy("="*60)
        self.log_deploy(f"⏪ 回滚后端到版本: {version}")
        self.log_deploy("="*60)
        
        try:
            self.log_deploy("\n🔐 连接服务器...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
            
            # 备份当前版本
            self.log_deploy("\n💾 备份当前版本...")
            backup_version = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ssh.exec_command(f'mkdir -p /root/server_versions/{backup_version}')
            stdin, stdout, stderr = ssh.exec_command(
                f'cp -r /root/Server/* /root/server_versions/{backup_version}/'
            )
            stdout.channel.recv_exit_status()
            self.log_deploy(f"  ✅ 已备份为: {backup_version}")
            
            # 清空当前目录
            self.log_deploy("\n🗑️ 清空当前目录...")
            stdin, stdout, stderr = ssh.exec_command('rm -rf /root/Server/*')
            stdout.channel.recv_exit_status()
            
            # 从历史版本复制
            self.log_deploy("\n📋 从历史版本复制...")
            stdin, stdout, stderr = ssh.exec_command(
                f'cp -r /root/server_versions/{version}/* /root/Server/'
            )
            exit_code = stdout.channel.recv_exit_status()
            
            if exit_code != 0:
                error = stderr.read().decode()
                raise Exception(f"复制失败: {error}")
            
            self.log_deploy("  ✅ 版本复制完成")
            
            # 重启服务
            self.log_deploy("\n🔄 重启 Docker 服务...")
            stdin, stdout, stderr = ssh.exec_command(
                'cd /root/Server && docker-compose restart backend'
            )
            stdout.channel.recv_exit_status()
            self.log_deploy("  ✅ 服务重启完成")
            
            # 健康检查
            self.log_deploy("\n🏥 健康检查...")
            import time
            time.sleep(5)
            stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/health')
            health_output = stdout.read().decode()
            if health_output and 'healthy' in health_output.lower():
                self.log_deploy(f"  ✅ API 健康检查通过: {health_output}")
            else:
                self.log_deploy(f"  ⚠️ API 可能未就绪: {health_output}")
            
            ssh.close()
            
            # 更新数据库
            self.log_deploy("\n💾 更新版本记录...")
            self.backend_db_manager.set_current_version(version)
            self.log_deploy("  ✅ 记录已更新")
            
            # 刷新列表
            self.refresh_backend_version_list()
            
            self.log_deploy("\n" + "="*60)
            self.log_deploy("🎉 回滚完成！")
            self.log_deploy("="*60)
            
            MessageBox("回滚成功", f"已成功回滚到版本 {version}", self).exec()
            
        except Exception as e:
            self.log_deploy(f"\n❌ 回滚失败: {e}")
            InfoBar.error("回滚失败", str(e), parent=self)
    
    def delete_backend_version(self):
        """删除选中的后端版本"""
        row = self.backend_version_table.currentRow()
        if row < 0:
            InfoBar.warning("未选择版本", "请先选择要删除的版本", parent=self)
            return
        
        dep = self.backend_version_table.item(row, 0).data(Qt.UserRole)
        version = dep['version']
        
        if dep['is_current']:
            InfoBar.warning("无法删除", "不能删除当前正在使用的版本", parent=self)
            return
        
        w = MessageBox(
            '确认删除',
            f"确定要删除版本: {version}？\n\n"
            f"这将同时删除服务器上的版本文件！\n此操作不可恢复！",
            self
        )
        
        if not w.exec():
            return
        
        try:
            self.log_deploy(f"\n🗑️ 删除版本: {version}")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            
            stdin, stdout, stderr = ssh.exec_command(f'rm -rf /root/server_versions/{version}')
            stdout.channel.recv_exit_status()
            ssh.close()
            
            self.log_deploy(f"  ✅ 服务器文件已删除")
            
            # 删除数据库记录
            self.backend_db_manager.delete_deployment(version)
            self.log_deploy(f"  ✅ 版本记录已删除")
            
            # 刷新列表
            self.refresh_backend_version_list()
            
            MessageBox("删除成功", f"版本 {version} 已删除", self).exec()
            
        except Exception as e:
            self.log_deploy(f"  ❌ 删除失败: {e}")
            InfoBar.error("删除失败", str(e), parent=self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())
