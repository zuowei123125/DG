#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动部署工具（跳过组管理功能）
"""
import sys
from PyQt5.QtWidgets import QApplication
from admin_gui import AdminWindow

if __name__ == "__main__":
    print("="*60)
    print("🚀 启动部署工具...")
    print("="*60)
    print("\n💡 提示：如果看到后端 API 错误，可以忽略")
    print("   部署功能不依赖后端 API，可以正常使用\n")
    
    app = QApplication(sys.argv)
    window = AdminWindow()
    
    # 直接切换到部署标签页
    # FluentWindow uses switchTo
    window.switchTo(window.deploy_interface)
    
    # 启用标签页（即使连接失败）
    # FluentWindow handles navigation enabling differently, but generally it's enabled by default
    # window.tabs.setEnabled(True) # No longer needed/available
    
    window.show()
    
    print("✅ 工具已启动")
    print("   请切换到「自动化部署」标签页开始使用\n")
    
    sys.exit(app.exec())

