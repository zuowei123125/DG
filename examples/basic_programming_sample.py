"""
基础编程示例 / Basic Programming Sample
===========================================

本文件展示了 Python 编程的核心概念和最佳实践。
This file demonstrates core Python programming concepts and best practices.

主要内容 / Contents:
1. 数据类型和变量 / Data Types and Variables
2. 函数定义和使用 / Function Definition and Usage
3. 类和对象 / Classes and Objects
4. 错误处理 / Error Handling
5. 文件操作 / File Operations
6. API 调用示例 / API Call Examples

作者 / Author: DesignerCEP Team
日期 / Date: 2025-12-27
"""

import json
import os
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path


# ============================================
# 第一部分：基础数据类型 / Part 1: Basic Data Types
# ============================================

def demonstrate_basic_types():
    """
    演示基本数据类型的使用
    Demonstrates the usage of basic data types
    """
    # 整数 / Integer
    age: int = 25
    
    # 浮点数 / Float
    price: float = 99.99
    
    # 字符串 / String
    name: str = "张三"
    
    # 布尔值 / Boolean
    is_active: bool = True
    
    # 列表 / List
    colors: List[str] = ["红色", "绿色", "蓝色"]
    
    # 字典 / Dictionary
    user: Dict[str, Any] = {
        "username": "zhangsan",
        "age": 25,
        "email": "zhangsan@example.com"
    }
    
    print("=== 基础数据类型演示 / Basic Data Types ===")
    print(f"姓名 / Name: {name}")
    print(f"年龄 / Age: {age}")
    print(f"价格 / Price: {price}")
    print(f"激活状态 / Active: {is_active}")
    print(f"颜色列表 / Colors: {colors}")
    print(f"用户信息 / User Info: {user}")
    print()


# ============================================
# 第二部分：函数 / Part 2: Functions
# ============================================

def calculate_total(price: float, quantity: int, discount: float = 0.0) -> float:
    """
    计算总价（含折扣）
    Calculate total price with discount
    
    Args:
        price: 单价 / Unit price
        quantity: 数量 / Quantity
        discount: 折扣率 (0-1) / Discount rate (0-1)
    
    Returns:
        float: 总价 / Total price
    """
    subtotal = price * quantity
    total = subtotal * (1 - discount)
    return round(total, 2)


def greet_user(name: str, greeting: str = "你好") -> str:
    """
    生成问候语
    Generate greeting message
    
    Args:
        name: 用户名 / Username
        greeting: 问候语 / Greeting phrase
    
    Returns:
        str: 完整的问候消息 / Complete greeting message
    """
    return f"{greeting}, {name}!"


# ============================================
# 第三部分：类和对象 / Part 3: Classes and Objects
# ============================================

class User:
    """
    用户类 / User Class
    
    演示面向对象编程的基本概念
    Demonstrates basic object-oriented programming concepts
    """
    
    def __init__(self, username: str, email: str, role: str = "user"):
        """
        初始化用户对象
        Initialize user object
        
        Args:
            username: 用户名 / Username
            email: 邮箱 / Email
            role: 角色 / Role (default: "user")
        """
        self.username = username
        self.email = email
        self.role = role
        self.created_at = datetime.now()
        self.points = 0
    
    def add_points(self, points: int) -> None:
        """
        增加积分
        Add points
        
        Args:
            points: 要增加的积分数 / Points to add
        """
        if points < 0:
            raise ValueError("积分不能为负数 / Points cannot be negative")
        self.points += points
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取用户信息
        Get user information
        
        Returns:
            Dict: 用户信息字典 / User info dictionary
        """
        return {
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "points": self.points,
            "created_at": self.created_at.isoformat()
        }
    
    def __str__(self) -> str:
        """字符串表示 / String representation"""
        return f"User(username='{self.username}', role='{self.role}', points={self.points})"


class VIPUser(User):
    """
    VIP 用户类（继承自 User）
    VIP User Class (inherits from User)
    """
    
    def __init__(self, username: str, email: str, vip_level: int = 1):
        """
        初始化 VIP 用户
        Initialize VIP user
        
        Args:
            username: 用户名 / Username
            email: 邮箱 / Email
            vip_level: VIP 等级 / VIP level
        """
        super().__init__(username, email, role="vip")
        self.vip_level = vip_level
    
    def add_points(self, points: int) -> None:
        """
        VIP 用户获得双倍积分
        VIP users get double points
        
        Args:
            points: 基础积分 / Base points
        """
        # VIP 用户获得双倍积分
        multiplier = 1 + (self.vip_level * 0.5)
        bonus_points = int(points * multiplier)
        super().add_points(bonus_points)
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取 VIP 用户信息
        Get VIP user information
        """
        info = super().get_info()
        info["vip_level"] = self.vip_level
        return info


# ============================================
# 第四部分：错误处理 / Part 4: Error Handling
# ============================================

def safe_divide(a: float, b: float) -> Optional[float]:
    """
    安全的除法操作（带错误处理）
    Safe division operation with error handling
    
    Args:
        a: 被除数 / Dividend
        b: 除数 / Divisor
    
    Returns:
        Optional[float]: 结果或 None（出错时）/ Result or None (on error)
    """
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print(f"错误 / Error: 不能除以零 / Cannot divide by zero")
        return None
    except TypeError as e:
        print(f"错误 / Error: 类型错误 / Type error - {e}")
        return None
    except Exception as e:
        print(f"未知错误 / Unknown error: {e}")
        return None


def read_json_file(filepath: str) -> Optional[Dict]:
    """
    读取 JSON 文件（带错误处理）
    Read JSON file with error handling
    
    Args:
        filepath: 文件路径 / File path
    
    Returns:
        Optional[Dict]: JSON 数据或 None / JSON data or None
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"错误 / Error: 文件未找到 / File not found - {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"错误 / Error: JSON 格式错误 / Invalid JSON - {e}")
        return None
    except Exception as e:
        print(f"读取文件失败 / Failed to read file: {e}")
        return None


# ============================================
# 第五部分：文件操作 / Part 5: File Operations
# ============================================

def save_user_data(user: User, directory: str = "data") -> bool:
    """
    保存用户数据到文件
    Save user data to file
    
    Args:
        user: 用户对象 / User object
        directory: 保存目录 / Save directory
    
    Returns:
        bool: 是否成功 / Success status
    """
    try:
        # 确保目录存在 / Ensure directory exists
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # 构建文件路径 / Build file path
        filepath = os.path.join(directory, f"{user.username}.json")
        
        # 保存数据 / Save data
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(user.get_info(), f, ensure_ascii=False, indent=2)
        
        print(f"✓ 用户数据已保存 / User data saved: {filepath}")
        return True
    except Exception as e:
        print(f"✗ 保存失败 / Save failed: {e}")
        return False


def load_user_data(username: str, directory: str = "data") -> Optional[Dict]:
    """
    从文件加载用户数据
    Load user data from file
    
    Args:
        username: 用户名 / Username
        directory: 数据目录 / Data directory
    
    Returns:
        Optional[Dict]: 用户数据或 None / User data or None
    """
    filepath = os.path.join(directory, f"{username}.json")
    return read_json_file(filepath)


# ============================================
# 第六部分：实用工具函数 / Part 6: Utility Functions
# ============================================

def format_currency(amount: float, currency: str = "CNY") -> str:
    """
    格式化货币显示
    Format currency display
    
    Args:
        amount: 金额 / Amount
        currency: 货币代码 / Currency code
    
    Returns:
        str: 格式化的货币字符串 / Formatted currency string
    """
    currency_symbols = {
        "CNY": "¥",
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    Validate email format
    
    Args:
        email: 邮箱地址 / Email address
    
    Returns:
        bool: 是否有效 / Is valid
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_timestamp() -> str:
    """
    获取当前时间戳
    Get current timestamp
    
    Returns:
        str: ISO 格式时间戳 / ISO format timestamp
    """
    return datetime.now().isoformat()


# ============================================
# 主程序 / Main Program
# ============================================

def main():
    """
    主函数 - 运行所有示例
    Main function - Run all examples
    """
    print("=" * 60)
    print("基础编程示例程序 / Basic Programming Sample Program")
    print("=" * 60)
    print()
    
    # 1. 演示基础数据类型
    demonstrate_basic_types()
    
    # 2. 演示函数使用
    print("=== 函数示例 / Function Examples ===")
    total = calculate_total(100, 3, 0.1)
    print(f"总价 / Total: {format_currency(total)}")
    print(greet_user("李明", "早上好"))
    print()
    
    # 3. 演示类和对象
    print("=== 类和对象示例 / Classes and Objects ===")
    
    # 创建普通用户
    user1 = User("zhangsan", "zhangsan@example.com")
    user1.add_points(100)
    print(f"普通用户 / Regular User: {user1}")
    print(f"用户信息 / User Info: {json.dumps(user1.get_info(), ensure_ascii=False, indent=2)}")
    print()
    
    # 创建 VIP 用户
    vip_user = VIPUser("lisi", "lisi@example.com", vip_level=2)
    vip_user.add_points(100)  # VIP 获得更多积分
    print(f"VIP 用户 / VIP User: {vip_user}")
    print(f"VIP 信息 / VIP Info: {json.dumps(vip_user.get_info(), ensure_ascii=False, indent=2)}")
    print()
    
    # 4. 演示错误处理
    print("=== 错误处理示例 / Error Handling ===")
    result1 = safe_divide(10, 2)
    print(f"10 ÷ 2 = {result1}")
    
    result2 = safe_divide(10, 0)
    print(f"10 ÷ 0 = {result2}")
    print()
    
    # 5. 演示文件操作
    print("=== 文件操作示例 / File Operations ===")
    
    # 保存用户数据
    save_user_data(user1, directory="/tmp/programming_sample_data")
    save_user_data(vip_user, directory="/tmp/programming_sample_data")
    
    # 加载用户数据
    loaded_data = load_user_data("zhangsan", directory="/tmp/programming_sample_data")
    if loaded_data:
        print(f"加载的数据 / Loaded data: {json.dumps(loaded_data, ensure_ascii=False, indent=2)}")
    print()
    
    # 6. 演示实用工具函数
    print("=== 工具函数示例 / Utility Functions ===")
    print(f"邮箱验证 / Email validation: zhangsan@example.com -> {validate_email('zhangsan@example.com')}")
    print(f"邮箱验证 / Email validation: invalid-email -> {validate_email('invalid-email')}")
    print(f"当前时间 / Current time: {get_timestamp()}")
    print(f"货币格式化 / Currency format: {format_currency(12345.67)}")
    print(f"货币格式化 / Currency format: {format_currency(12345.67, 'USD')}")
    print()
    
    print("=" * 60)
    print("示例程序运行完成 / Sample program completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
