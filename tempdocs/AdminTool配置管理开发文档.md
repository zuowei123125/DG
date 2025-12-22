# AdminTool 系统配置管理开发文档

## 📋 开发需求

AdminTool需要集成系统配置管理功能，用于可视化管理：
1. 功能配置（积分价格、启用/禁用）
2. VIP配置（价格、配额、倍数）
3. 签到配置（连续天数奖励）
4. 数据统计（今日统计、功能使用排行）

---

## 🎨 技术方案

### 方案A：使用 qfluentwidgets（推荐）

#### 1. 安装依赖

```bash
pip install PyQt-Fluent-Widgets
```

#### 2. 改造现有代码

**主窗口改造** (`admin_gui.py`):
```python
from qfluentwidgets import FluentWindow, FluentIcon, NavigationItemPosition

class AdminWindow(FluentWindow):  # 改为继承 FluentWindow
    def __init__(self):
        super().__init__()
        
        # 启用 Mica 效果
        self.setMicaEffectEnabled(True)
        
        # 添加配置管理页面
        self.config_interface = ConfigInterface(self.api_client, self)
        
        self.addSubInterface(
            self.config_interface,
            icon=FluentIcon.SETTING,
            text="系统配置",
            position=NavigationItemPosition.BOTTOM
        )
```

**配置管理界面** (`config_interface.py`，新建):
```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (
    Pivot, PushButton, TableWidget, CardWidget,
    MessageBox, InfoBar
)

class ConfigInterface(QWidget):
    """配置管理主界面"""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        
        # 创建Pivot导航
        self.pivot = Pivot(self)
        
        # 添加子页面
        self.features_tab = FeaturesConfigTab(api_client)
        self.vip_tab = VIPConfigTab(api_client)
        self.checkin_tab = CheckInConfigTab(api_client)
        self.stats_tab = StatsTab(api_client)
        
        # 添加到Pivot
        self.pivot.addItem('features', '功能配置', self.features_tab)
        self.pivot.addItem('vip', 'VIP配置', self.vip_tab)
        self.pivot.addItem('checkin', '签到配置', self.checkin_tab)
        self.pivot.addItem('stats', '数据统计', self.stats_tab)


class FeaturesConfigTab(QWidget):
    """功能配置标签页"""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        
        # 表格
        self.table = TableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "功能名称", "普通价格", "VIP价格", "SVIP价格", "状态", "操作"
        ])
        
        # 按钮
        self.btn_add = PushButton("新增功能", self)
        self.btn_refresh = PushButton("刷新", self)
        
        self.load_data()
    
    def load_data(self):
        """从API加载数据"""
        try:
            resp = requests.get(
                f"{self.api_client.base_url}/admin/config/features",
                headers=self.api_client.get_headers()
            )
            data = resp.json()
            # 填充表格...
            InfoBar.success("加载成功", f"已加载 {len(data)} 个功能")
        except Exception as e:
            MessageBox("错误", f"加载失败: {e}", self).exec()
```

---

### 方案B：使用现有PyQt5（快速实现）

如果不想安装新依赖，可以在现有 `admin_gui.py` 基础上：

#### 1. 在 `setup_` 中添加新标签页

```python
def __init__(self):
    # ... 现有代码 ...
    
    # 新增第4个标签页
    self.config_tab = QWidget()
    self.setup_config_tab()
    self.tabs.addTab(self.config_tab, "系统配置")

def setup_config_tab(self):
    """设置系统配置标签页"""
    layout = QVBoxLayout(self.config_tab)
    
    # 子标签页
    sub_tabs = QTabWidget()
    
    # 功能配置
    features_widget = QWidget()
    self.setup_features_config(features_widget)
    sub_tabs.addTab(features_widget, "功能配置")
    
    # VIP配置
    vip_widget = QWidget()
    self.setup_vip_config(vip_widget)
    sub_tabs.addTab(vip_widget, "VIP配置")
    
    # 签到配置
    checkin_widget = QWidget()
    self.setup_checkin_config(checkin_widget)
    sub_tabs.addTab(checkin_widget, "签到配置")
    
    # 统计
    stats_widget = QWidget()
    self.setup_stats(stats_widget)
    sub_tabs.addTab(stats_widget, "数据统计")
    
    layout.addWidget(sub_tabs)
```

#### 2. 实现各个子界面

```python
def setup_features_config(self, widget):
    """功能配置界面"""
    layout = QVBoxLayout(widget)
    
    # 操作按钮
    btn_layout = QHBoxLayout()
    btn_add = QPushButton("新增功能")
    btn_add.clicked.connect(self.add_feature_config)
    btn_refresh = QPushButton("刷新")
    btn_refresh.clicked.connect(self.refresh_features_config)
    btn_layout.addWidget(btn_add)
    btn_layout.addWidget(btn_refresh)
    btn_layout.addStretch()
    layout.addLayout(btn_layout)
    
    # 表格
    self.features_table = QTableWidget()
    self.features_table.setColumnCount(7)
    self.features_table.setHorizontalHeaderLabels([
        "功能名称", "分类", "普通价格", "VIP价格", "SVIP价格", "状态", "操作"
    ])
    self.features_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    layout.addWidget(self.features_table)
    
    # 加载数据
    self.refresh_features_config()

def refresh_features_config(self):
    """刷新功能配置"""
    try:
        resp = requests.get(
            f"{self.api_client.base_url}/admin/config/features",
            headers=self.api_client.get_headers()
        )
        resp.raise_for_status()
        data = resp.json()
        
        self.features_table.setRowCount(len(data))
        for i, feature in enumerate(data):
            self.features_table.setItem(i, 0, QTableWidgetItem(feature['feature_name']))
            self.features_table.setItem(i, 1, QTableWidgetItem(feature['category']))
            self.features_table.setItem(i, 2, QTableWidgetItem(str(feature['points_cost'])))
            self.features_table.setItem(i, 3, QTableWidgetItem(str(feature['vip_points_cost'])))
            self.features_table.setItem(i, 4, QTableWidgetItem(str(feature['svip_points_cost'])))
            self.features_table.setItem(i, 5, QTableWidgetItem("✓" if feature['enabled'] else "✗"))
            
            # 操作按钮
            btn_edit = QPushButton("编辑")
            btn_edit.clicked.connect(lambda checked, f=feature: self.edit_feature_config(f))
            self.features_table.setCellWidget(i, 6, btn_edit)
        
        QMessageBox.information(self, "成功", f"已加载 {len(data)} 个功能配置")
    except Exception as e:
        QMessageBox.critical(self, "错误", f"加载失败: {e}")

def edit_feature_config(self, feature):
    """编辑功能配置"""
    dialog = QDialog(self)
    dialog.setWindowTitle(f"编辑功能: {feature['feature_name']}")
    layout = QFormLayout(dialog)
    
    # 输入框
    points_input = QSpinBox()
    points_input.setRange(0, 9999)
    points_input.setValue(feature['points_cost'])
    layout.addRow("普通用户积分:", points_input)
    
    vip_points_input = QSpinBox()
    vip_points_input.setRange(0, 9999)
    vip_points_input.setValue(feature['vip_points_cost'])
    layout.addRow("VIP积分:", vip_points_input)
    
    svip_points_input = QSpinBox()
    svip_points_input.setRange(0, 9999)
    svip_points_input.setValue(feature['svip_points_cost'])
    layout.addRow("SVIP积分:", svip_points_input)
    
    enabled_check = QCheckBox()
    enabled_check.setChecked(feature['enabled'])
    layout.addRow("启用:", enabled_check)
    
    # 按钮
    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addRow(buttons)
    
    if dialog.exec() == QDialog.Accepted:
        # 提交更新
        try:
            resp = requests.put(
                f"{self.api_client.base_url}/admin/config/features/{feature['feature_key']}",
                json={
                    "points_cost": points_input.value(),
                    "vip_points_cost": vip_points_input.value(),
                    "svip_points_cost": svip_points_input.value(),
                    "enabled": enabled_check.isChecked()
                },
                headers=self.api_client.get_headers()
            )
            resp.raise_for_status()
            QMessageBox.information(self, "成功", "更新成功")
            self.refresh_features_config()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"更新失败: {e}")
```

---

## 📊 API接口参考

### 功能配置API

```python
# 获取所有功能
GET /api/v1/admin/config/features
Headers: x-admin-token: admin-secret-token

# 新增功能
POST /api/v1/admin/config/features
Body: {
    "feature_key": "new_feature",
    "feature_name": "新功能",
    "category": "ai",
    "points_cost": 60,
    "vip_points_cost": 0,
    "svip_points_cost": 0
}

# 更新功能
PUT /api/v1/admin/config/features/{feature_key}
Body: {
    "points_cost": 80,
    "enabled": true
}
```

### VIP配置API

```python
# 获取VIP配置
GET /api/v1/admin/config/vip

# 更新VIP配置
PUT /api/v1/admin/config/vip/vip
Body: {
    "price": 35.00,
    "daily_quota": 25,
    "points_multiplier": 1.60
}
```

### 签到配置API

```python
# 获取签到配置
GET /api/v1/admin/config/checkin

# 新增档位
POST /api/v1/admin/config/checkin
Body: {
    "consecutive_days": 60,
    "base_points": 10,
    "bonus_points": 150,
    "total_points": 160
}

# 更新档位
PUT /api/v1/admin/config/checkin/7
Body: {
    "bonus_points": 25,
    "total_points": 35
}
```

### 统计API

```python
# 今日统计
GET /api/v1/admin/stats/today

# 功能使用排行
GET /api/v1/admin/stats/feature-usage?days=7

# 积分趋势
GET /api/v1/admin/stats/points-trend?days=7
```

---

## ✅ 开发检查清单

- [ ] 安装依赖（如使用方案A）
- [ ] 改造主窗口类
- [ ] 创建配置管理界面
- [ ] 实现功能配置CRUD
- [ ] 实现VIP配置编辑
- [ ] 实现签到配置编辑
- [ ] 实现数据统计展示
- [ ] 连接后端API
- [ ] 错误处理和提示
- [ ] 测试所有功能

---

## 📝 注意事项

1. **权限验证**: 所有管理接口都需要 `x-admin-token: admin-secret-token`
2. **错误处理**: 使用 try-except 捕获网络异常
3. **用户友好**: 操作前确认，操作后提示
4. **数据刷新**: 修改后自动刷新列表
5. **布局美观**: 合理使用Grid/Box布局

---

## 🎯 优先级

### P0（必须）
- 功能配置查看和编辑
- VIP配置编辑
- 签到配置编辑

### P1（重要）
- 功能配置新增/删除
- 签到配置新增/删除
- 数据统计展示

### P2（可选）
- Fluent Design 风格改造
- 图表可视化
- 高级筛选和搜索

---

**开发愉快！如有问题请参考主文档或API文档。**

