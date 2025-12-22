import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QHeaderView, QTableWidgetItem, QFrame,
    QGridLayout, QLabel
)
from PyQt5.QtCore import Qt
from qfluentwidgets import (
    Pivot, PushButton, TableWidget, CardWidget,
    MessageBox, InfoBar, LineEdit, SpinBox, CheckBox, ComboBox,
    FluentIcon as FIF, SubtitleLabel, CaptionLabel,
    ScrollArea, BodyLabel, PrimaryPushButton, MessageBoxBase, StrongBodyLabel
)

class ConfigDialog(MessageBoxBase):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(title, self)
        self.viewLayout.addWidget(self.titleLabel)
        self.widget.setMinimumWidth(350)
        self.yesButton.setText("确定")
        self.cancelButton.setText("取消")

    def add_row(self, label_text, widget):
        self.viewLayout.addWidget(StrongBodyLabel(label_text, self))
        self.viewLayout.addWidget(widget)

class ConfigInterface(QWidget):
    """配置管理主界面"""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        
        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        
        # 标题
        self.title_label = SubtitleLabel("系统配置", self)
        self.main_layout.addWidget(self.title_label)
        
        # Pivot 导航
        self.pivot = Pivot(self)
        self.main_layout.addWidget(self.pivot)
        
        # 堆叠窗口容器
        self.stacked_widget = QWidget()
        self.stacked_layout = QVBoxLayout(self.stacked_widget)
        self.stacked_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.stacked_widget)
        
        # 子页面
        self.features_tab = FeaturesConfigTab(api_client, self)
        self.vip_tab = VIPConfigTab(api_client, self)
        self.checkin_tab = CheckInConfigTab(api_client, self)
        self.stats_tab = StatsTab(api_client, self)
        
        # 添加子页面到 Pivot
        self.add_sub_interface(self.features_tab, 'features', '功能配置')
        self.add_sub_interface(self.vip_tab, 'vip', 'VIP配置')
        self.add_sub_interface(self.checkin_tab, 'checkin', '签到配置')
        self.add_sub_interface(self.stats_tab, 'stats', '数据统计')
        
        # 初始化显示第一个
        self.pivot.setCurrentItem(self.features_tab.objectName())
        self.pivot.currentItemChanged.connect(self.on_pivot_changed)
        
        # 初始加载
        self.features_tab.setVisible(True)
        self.vip_tab.setVisible(False)
        self.checkin_tab.setVisible(False)
        self.stats_tab.setVisible(False)
        
        # 默认布局填充
        self.stacked_layout.addWidget(self.features_tab)
        self.stacked_layout.addWidget(self.vip_tab)
        self.stacked_layout.addWidget(self.checkin_tab)
        self.stacked_layout.addWidget(self.stats_tab)

    def add_sub_interface(self, widget, object_name, text):
        widget.setObjectName(object_name)
        self.pivot.addItem(routeKey=object_name, text=text)

    def on_pivot_changed(self, route_key):
        self.features_tab.setVisible(route_key == 'features')
        self.vip_tab.setVisible(route_key == 'vip')
        self.checkin_tab.setVisible(route_key == 'checkin')
        self.stats_tab.setVisible(route_key == 'stats')
        
        # 刷新数据
        if route_key == 'features':
            self.features_tab.load_data()
        elif route_key == 'vip':
            self.vip_tab.load_data()
        elif route_key == 'checkin':
            self.checkin_tab.load_data()
        elif route_key == 'stats':
            self.stats_tab.load_data()

class FeaturesConfigTab(QWidget):
    """功能配置标签页"""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.init_ui()
        
    def init_ui(self):
        self.v_layout = QVBoxLayout(self)
        
        # 工具栏
        self.tool_layout = QHBoxLayout()
        self.btn_refresh = PushButton(FIF.SYNC, "刷新", self)
        self.btn_refresh.clicked.connect(self.load_data)
        
        self.btn_add = PrimaryPushButton(FIF.ADD, "新增功能", self)
        self.btn_add.clicked.connect(self.add_feature)
        
        self.tool_layout.addWidget(self.btn_refresh)
        self.tool_layout.addWidget(self.btn_add)
        self.tool_layout.addStretch(1)
        self.v_layout.addLayout(self.tool_layout)
        
        # 表格
        self.table = TableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Key", "功能名称", "分类", "普通价格", "VIP价格", "SVIP价格", "状态"
        ])
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(TableWidget.SelectRows)
        self.table.setEditTriggers(TableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_feature)
        
        self.v_layout.addWidget(self.table)
        
    def load_mock_data(self):
        """加载模拟数据"""
        data = [
            (1, 10, 0, 10),
            (2, 10, 5, 15),
            (3, 10, 10, 20),
            (7, 10, 50, 60),
        ]
        self.table.setRowCount(len(data))
        for i, (days, base, bonus, total) in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(f"{days} 天"))
            self.table.setItem(i, 1, QTableWidgetItem(str(base)))
            self.table.setItem(i, 2, QTableWidgetItem(str(bonus)))
            self.table.setItem(i, 3, QTableWidgetItem(str(total)))

    def load_data(self):
        if not self.api_client:
            InfoBar.warning("未连接", "请先连接到后端服务器", parent=self)
            return
            
        try:
            resp = requests.get(f"{self.api_client.base_url}/admin/config/features", headers=self.api_client.get_headers(), timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            self.table.setRowCount(len(data))
            for i, item in enumerate(data):
                self.table.setItem(i, 0, QTableWidgetItem(item.get('feature_key', '')))
                self.table.setItem(i, 1, QTableWidgetItem(item.get('feature_name', '')))
                self.table.setItem(i, 2, QTableWidgetItem(item.get('category', '')))
                self.table.setItem(i, 3, QTableWidgetItem(str(item.get('points_cost', 0))))
                self.table.setItem(i, 4, QTableWidgetItem(str(item.get('vip_points_cost', 0))))
                self.table.setItem(i, 5, QTableWidgetItem(str(item.get('svip_points_cost', 0))))
                
                enabled = item.get('enabled', False)
                status_item = QTableWidgetItem("启用" if enabled else "禁用")
                if enabled:
                    status_item.setForeground(Qt.darkGreen)
                else:
                    status_item.setForeground(Qt.red)
                self.table.setItem(i, 6, status_item)
                
                # Store full data
                self.table.item(i, 0).setData(Qt.UserRole, item)
                
            InfoBar.success("加载成功", f"已加载 {len(data)} 个功能配置", parent=self)
            
        except Exception as e:
            InfoBar.error("加载失败", f"无法加载功能配置: {str(e)}", parent=self)
            print(f"Error loading config: {e}")

    def add_feature(self):
        dialog = ConfigDialog("新增功能", self)
        
        key_edit = LineEdit()
        name_edit = LineEdit()
        category_edit = LineEdit()
        points_spin = SpinBox()
        points_spin.setRange(0, 9999)
        vip_spin = SpinBox()
        vip_spin.setRange(0, 9999)
        svip_spin = SpinBox()
        svip_spin.setRange(0, 9999)
        
        dialog.add_row("Key (唯一标识):", key_edit)
        dialog.add_row("功能名称:", name_edit)
        dialog.add_row("分类:", category_edit)
        dialog.add_row("积分消耗:", points_spin)
        dialog.add_row("VIP消耗:", vip_spin)
        dialog.add_row("SVIP消耗:", svip_spin)
        
        if dialog.exec():
            key = key_edit.text().strip()
            name = name_edit.text().strip()
            if not key or not name:
                InfoBar.warning("输入错误", "Key和名称不能为空", parent=self)
                return
                
            payload = {
                "feature_key": key,
                "feature_name": name,
                "category": category_edit.text().strip(),
                "points_cost": points_spin.value(),
                "vip_points_cost": vip_spin.value(),
                "svip_points_cost": svip_spin.value(),
                "enabled": True
            }
            
            try:
                resp = requests.post(f"{self.api_client.base_url}/admin/config/features", json=payload, headers=self.api_client.get_headers(), timeout=10)
                resp.raise_for_status()
                InfoBar.success("成功", f"功能 '{name}' 已添加", parent=self)
                self.load_data()
            except Exception as e:
                InfoBar.error("失败", f"添加失败: {str(e)}", parent=self)

    def edit_feature(self):
        row = self.table.currentRow()
        if row < 0: return
        item = self.table.item(row, 0).data(Qt.UserRole)
        
        dialog = ConfigDialog(f"编辑功能: {item['feature_name']}", self)
        
        points_spin = SpinBox()
        points_spin.setRange(0, 9999)
        points_spin.setValue(item.get('points_cost', 0))
        
        vip_spin = SpinBox()
        vip_spin.setRange(0, 9999)
        vip_spin.setValue(item.get('vip_points_cost', 0))
        
        svip_spin = SpinBox()
        svip_spin.setRange(0, 9999)
        svip_spin.setValue(item.get('svip_points_cost', 0))
        
        enabled_check = CheckBox("启用")
        enabled_check.setChecked(item.get('enabled', True))
        
        dialog.add_row("积分消耗:", points_spin)
        dialog.add_row("VIP消耗:", vip_spin)
        dialog.add_row("SVIP消耗:", svip_spin)
        dialog.viewLayout.addWidget(enabled_check)
        
        if dialog.exec():
            payload = {
                "points_cost": points_spin.value(),
                "vip_points_cost": vip_spin.value(),
                "svip_points_cost": svip_spin.value(),
                "enabled": enabled_check.isChecked()
            }
            try:
                resp = requests.put(f"{self.api_client.base_url}/admin/config/features/{item['feature_key']}", json=payload, headers=self.api_client.get_headers(), timeout=10)
                resp.raise_for_status()
                InfoBar.success("成功", "配置已更新", parent=self)
                self.load_data()
            except Exception as e:
                InfoBar.error("失败", f"更新失败: {str(e)}", parent=self)

class VIPConfigTab(QWidget):
    """VIP配置标签页"""
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.v_layout = QVBoxLayout(self)
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        
        self.card = CardWidget(self)
        self.card_layout = QGridLayout(self.card)
        self.card_layout.setContentsMargins(20, 20, 20, 20)
        self.card_layout.setSpacing(20)
        
        self.price_spin = SpinBox()
        self.price_spin.setRange(0, 9999)
        self.price_spin.setValue(35)
        self.card_layout.addWidget(StrongBodyLabel("VIP 价格 (元/月):", self.card), 0, 0)
        self.card_layout.addWidget(self.price_spin, 0, 1)
        
        self.quota_spin = SpinBox()
        self.quota_spin.setRange(0, 9999)
        self.quota_spin.setValue(25)
        self.card_layout.addWidget(StrongBodyLabel("每日配额 (次):", self.card), 1, 0)
        self.card_layout.addWidget(self.quota_spin, 1, 1)
        
        self.multiplier_spin = SpinBox() 
        self.multiplier_spin.setRange(100, 1000)
        self.multiplier_spin.setValue(160) 
        self.card_layout.addWidget(StrongBodyLabel("积分倍数 (%):", self.card), 2, 0)
        self.card_layout.addWidget(self.multiplier_spin, 2, 1)
        
        self.btn_save = PrimaryPushButton(FIF.SAVE, "保存配置", self.card)
        self.btn_save.clicked.connect(self.save_data)
        self.card_layout.addWidget(self.btn_save, 3, 0, 1, 2)
        
        self.v_layout.addWidget(self.card)
        self.v_layout.addStretch(1)
        
    def load_data(self):
        if not self.api_client:
            return
        try:
            resp = requests.get(f"{self.api_client.base_url}/admin/config/vip", headers=self.api_client.get_headers(), timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            # 查找VIP配置
            for item in data:
                if item.get('vip_type') == 'vip':
                    self.price_spin.setValue(int(item.get('price', 35)))
                    self.quota_spin.setValue(int(item.get('daily_quota', 25)))
                    self.multiplier_spin.setValue(int(item.get('points_multiplier', 1.6) * 100))
                    break
        except Exception as e:
            print(f"Load VIP config error: {e}")
        
    def save_data(self):
        if not self.api_client:
            InfoBar.warning("未连接", "请先连接到后端服务器", parent=self)
            return
        
        try:
            payload = {
                "price": self.price_spin.value(),
                "daily_quota": self.quota_spin.value(),
                "points_multiplier": self.multiplier_spin.value() / 100.0
            }
            resp = requests.put(f"{self.api_client.base_url}/admin/config/vip/vip", json=payload, headers=self.api_client.get_headers(), timeout=10)
            resp.raise_for_status()
            InfoBar.success("保存成功", "VIP配置已更新", parent=self)
        except Exception as e:
            InfoBar.error("保存失败", str(e), parent=self)

class CheckInConfigTab(QWidget):
    """签到配置标签页"""
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.v_layout = QVBoxLayout(self)
        
        self.btn_add = PrimaryPushButton(FIF.ADD, "新增签到规则", self)
        self.v_layout.addWidget(self.btn_add)
        
        self.table = TableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["连续天数", "基础积分", "额外奖励", "总计"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.v_layout.addWidget(self.table)
        
        self.load_mock_data()

    def load_mock_data(self):
        """加载模拟数据"""
        data = [
            (1, 10, 0, 10),
            (2, 10, 5, 15),
            (3, 10, 10, 20),
            (7, 10, 50, 60),
        ]
        self.table.setRowCount(len(data))
        for i, (days, base, bonus, total) in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(f"{days} 天"))
            self.table.setItem(i, 1, QTableWidgetItem(str(base)))
            self.table.setItem(i, 2, QTableWidgetItem(str(bonus)))
            self.table.setItem(i, 3, QTableWidgetItem(str(total)))

    def load_data(self):
        if not self.api_client:
            return
        try:
            resp = requests.get(f"{self.api_client.base_url}/admin/config/checkin", headers=self.api_client.get_headers(), timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            self.table.setRowCount(len(data))
            for i, item in enumerate(data):
                self.table.setItem(i, 0, QTableWidgetItem(f"{item.get('consecutive_days', 0)} 天"))
                self.table.setItem(i, 1, QTableWidgetItem(str(item.get('base_points', 0))))
                self.table.setItem(i, 2, QTableWidgetItem(str(item.get('bonus_points', 0))))
                self.table.setItem(i, 3, QTableWidgetItem(str(item.get('total_points', 0))))
                # Store full data
                self.table.item(i, 0).setData(Qt.UserRole, item)
                
            InfoBar.success("加载成功", f"已加载 {len(data)} 个签到规则", parent=self)
        except Exception as e:
            InfoBar.error("加载失败", str(e), parent=self)

class StatsTab(QWidget):
    """数据统计标签页"""
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.v_layout = QVBoxLayout(self)
        
        self.card = CardWidget(self)
        self.card_layout = QVBoxLayout(self.card)
        
        self.card_layout.addWidget(SubtitleLabel("今日数据概览", self.card))
        
        self.grid = QGridLayout()
        self.grid.addWidget(BodyLabel("今日活跃用户:"), 0, 0)
        self.lbl_active_users = StrongBodyLabel("-", self.card)
        self.grid.addWidget(self.lbl_active_users, 0, 1)
        
        self.grid.addWidget(BodyLabel("今日签到:"), 1, 0)
        self.lbl_checkins = StrongBodyLabel("-", self.card)
        self.grid.addWidget(self.lbl_checkins, 1, 1)
        
        self.grid.addWidget(BodyLabel("今日积分消耗:"), 2, 0)
        self.lbl_points = StrongBodyLabel("-", self.card)
        self.grid.addWidget(self.lbl_points, 2, 1)
        
        self.grid.addWidget(BodyLabel("今日功能调用:"), 3, 0)
        self.lbl_feature_usage = StrongBodyLabel("-", self.card)
        self.grid.addWidget(self.lbl_feature_usage, 3, 1)
        
        self.card_layout.addLayout(self.grid)
        
        # 刷新按钮
        self.btn_refresh = PrimaryPushButton(FIF.SYNC, "刷新统计", self.card)
        self.btn_refresh.clicked.connect(self.load_data)
        self.card_layout.addWidget(self.btn_refresh)
        
        self.v_layout.addWidget(self.card)
        self.v_layout.addStretch(1)

    def load_data(self):
        if not self.api_client:
            InfoBar.warning("未连接", "请先连接到后端服务器", parent=self)
            return
        
        try:
            resp = requests.get(f"{self.api_client.base_url}/admin/stats/today", headers=self.api_client.get_headers(), timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            self.lbl_active_users.setText(str(data.get('active_users', 0)))
            self.lbl_checkins.setText(str(data.get('check_ins', 0)))
            self.lbl_points.setText(str(data.get('points_consumed', 0)))
            self.lbl_feature_usage.setText(str(data.get('feature_usage', 0)))
            
            InfoBar.success("刷新成功", "统计数据已更新", parent=self)
        except Exception as e:
            InfoBar.error("加载失败", f"无法加载统计数据: {str(e)}", parent=self)
            print(f"Load stats error: {e}")
