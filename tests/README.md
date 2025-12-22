# DesignerCEP 测试套件

本目录包含前后端的完整测试代码。

## 目录结构

```
tests/
├── backend/          # 后端测试
│   ├── test_admin_config.py
│   ├── test_feature.py
│   ├── test_checkin.py
│   ├── test_user_profile.py
│   ├── test_stats.py
│   └── conftest.py
├── frontend/         # 前端测试
│   ├── HomePage.test.ts
│   ├── Profile.test.ts
│   ├── CheckIn.test.ts
│   └── utils.test.ts
├── integration/      # 集成测试
│   └── e2e.test.py
└── README.md         # 本文件
```

## 运行测试

### 后端测试
```bash
cd tests/backend
pytest -v
```

### 前端测试
```bash
cd Designer
npm run test
```

### 集成测试
```bash
cd tests/integration
pytest -v
```

## 测试覆盖率

- 后端API: 目标 > 80%
- 前端组件: 目标 > 70%
- 集成测试: 核心流程全覆盖

