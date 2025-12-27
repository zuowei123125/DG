"""
测试基础编程示例 / Test Basic Programming Sample
================================================

本文件测试 basic_programming_sample.py 中的核心功能
This file tests core functionality in basic_programming_sample.py
"""

import sys
import os

# Add parent directory to path to import the sample module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from examples.basic_programming_sample import (
    User, VIPUser, calculate_total, greet_user,
    safe_divide, validate_email, format_currency,
    get_timestamp
)


def test_calculate_total():
    """测试总价计算函数"""
    # 无折扣
    assert calculate_total(100, 2, 0) == 200.0
    # 10% 折扣
    assert calculate_total(100, 3, 0.1) == 270.0
    # 50% 折扣
    assert calculate_total(50, 4, 0.5) == 100.0
    print("✓ test_calculate_total passed")


def test_greet_user():
    """测试问候函数"""
    assert greet_user("张三") == "你好, 张三!"
    assert greet_user("李四", "早上好") == "早上好, 李四!"
    print("✓ test_greet_user passed")


def test_user_class():
    """测试 User 类"""
    user = User("testuser", "test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "user"
    assert user.points == 0
    
    # 测试增加积分
    user.add_points(50)
    assert user.points == 50
    
    user.add_points(30)
    assert user.points == 80
    
    # 测试获取信息
    info = user.get_info()
    assert info["username"] == "testuser"
    assert info["points"] == 80
    
    print("✓ test_user_class passed")


def test_vip_user_class():
    """测试 VIP User 类"""
    vip = VIPUser("vipuser", "vip@example.com", vip_level=2)
    assert vip.username == "vipuser"
    assert vip.role == "vip"
    assert vip.vip_level == 2
    
    # VIP 用户应该获得更多积分 (100 * (1 + 2 * 0.5) = 200)
    vip.add_points(100)
    assert vip.points == 200
    
    # 测试继承的方法
    info = vip.get_info()
    assert info["vip_level"] == 2
    assert info["points"] == 200
    
    print("✓ test_vip_user_class passed")


def test_safe_divide():
    """测试安全除法函数"""
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(9, 3) == 3.0
    assert safe_divide(10, 0) is None  # 除以零应返回 None
    assert safe_divide(1, 0.5) == 2.0
    print("✓ test_safe_divide passed")


def test_validate_email():
    """测试邮箱验证函数"""
    assert validate_email("test@example.com") is True
    assert validate_email("user123@gmail.com") is True
    assert validate_email("invalid-email") is False
    assert validate_email("@example.com") is False
    assert validate_email("test@") is False
    print("✓ test_validate_email passed")


def test_format_currency():
    """测试货币格式化函数"""
    assert format_currency(100) == "¥100.00"
    assert format_currency(1234.56) == "¥1,234.56"
    assert format_currency(100, "USD") == "$100.00"
    assert format_currency(100, "EUR") == "€100.00"
    print("✓ test_format_currency passed")


def test_timestamp():
    """测试时间戳函数"""
    from datetime import datetime
    
    timestamp = get_timestamp()
    assert isinstance(timestamp, str)
    assert len(timestamp) > 0
    
    # 检查是否是有效的 ISO 格式时间戳
    # 应该能够被解析为 datetime 对象
    try:
        parsed_time = datetime.fromisoformat(timestamp)
        # 检查是否是最近的时间（在过去 1 分钟内）
        now = datetime.now()
        time_diff = abs((now - parsed_time).total_seconds())
        assert time_diff < 60, "时间戳应该是当前时间 / Timestamp should be current time"
    except ValueError:
        assert False, "时间戳格式无效 / Invalid timestamp format"
    
    print("✓ test_timestamp passed")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("开始运行测试 / Running Tests")
    print("=" * 60)
    print()
    
    try:
        test_calculate_total()
        test_greet_user()
        test_user_class()
        test_vip_user_class()
        test_safe_divide()
        test_validate_email()
        test_format_currency()
        test_timestamp()
        
        print()
        print("=" * 60)
        print("✓ 所有测试通过！ / All tests passed!")
        print("=" * 60)
        return True
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"✗ 测试失败 / Test failed: {e}")
        print("=" * 60)
        return False
    except Exception as e:
        print()
        print("=" * 60)
        print(f"✗ 发生错误 / Error occurred: {e}")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
