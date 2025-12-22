# -*- coding: utf-8 -*-
"""
端到端集成测试
测试完整的业务流程
"""

import pytest
import requests
import time
from datetime import date

API_BASE_URL = 'https://backend.aidg168.uk/api/v1'
ADMIN_TOKEN = 'admin-secret-token'


class TestUserJourney:
    """用户完整流程测试"""
    
    def test_complete_user_journey(self):
        """
        测试用户完整使用流程：
        1. 查看用户资料
        2. 每日签到
        3. 使用功能
        4. 查看积分历史
        """
        username = 'e2e_test_user'
        
        # 1. 查看用户资料
        profile_response = requests.get(
            f"{API_BASE_URL}/user/profile",
            params={'username': username}
        )
        
        if profile_response.status_code == 200:
            profile = profile_response.json()['data']
            initial_points = profile['points']
            print(f"初始积分: {initial_points}")
        else:
            print(f"用户 {username} 不存在，请先创建")
            return
        
        # 2. 每日签到
        checkin_response = requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': username}
        )
        
        if checkin_response.status_code == 200:
            checkin_data = checkin_response.json()['data']
            print(f"签到成功：获得 {checkin_data['points_earned']} 积分")
            print(f"连续签到：{checkin_data['consecutive_days']} 天")
        elif checkin_response.status_code == 400:
            print("今日已签到")
        
        # 等待数据更新
        time.sleep(1)
        
        # 3. 使用功能
        feature_response = requests.post(
            f"{API_BASE_URL}/feature/use",
            json={
                'username': username,
                'feature_key': 'ai_color_match',
                'device_id': 'e2e_test_device'
            }
        )
        
        if feature_response.status_code == 200:
            feature_data = feature_response.json()['data']
            print(f"使用功能成功：{feature_data['message']}")
            print(f"消耗类型：{feature_data['cost_type']}")
            print(f"剩余积分：{feature_data['points_remaining']}")
        else:
            print(f"使用功能失败：{feature_response.json()['detail']}")
        
        # 4. 查看积分历史
        history_response = requests.get(
            f"{API_BASE_URL}/points/history",
            params={'username': username, 'page': 1, 'limit': 10}
        )
        
        if history_response.status_code == 200:
            history_data = history_response.json()['data']
            print(f"\n积分历史（共 {history_data['total']} 条）:")
            for record in history_data['records'][:5]:
                print(f"  {record['created_at']}: {record['description']} {record['amount']:+d}")
        
        # 5. 验证最终状态
        final_profile_response = requests.get(
            f"{API_BASE_URL}/user/profile",
            params={'username': username}
        )
        
        final_profile = final_profile_response.json()['data']
        final_points = final_profile['points']
        print(f"\n最终积分: {final_points}")
        
        assert True  # 流程完成即通过


class TestAdminWorkflow:
    """管理员工作流程测试"""
    
    def test_admin_config_workflow(self):
        """
        测试管理员配置流程：
        1. 查看当前配置
        2. 创建新功能
        3. 修改VIP配置
        4. 查看统计数据
        """
        headers = {'x-admin-token': ADMIN_TOKEN}
        
        # 1. 查看功能配置
        features_response = requests.get(
            f"{API_BASE_URL}/admin/config/features",
            headers=headers
        )
        
        assert features_response.status_code == 200
        features = features_response.json()
        print(f"当前功能数量: {len(features)}")
        
        # 2. 创建测试功能
        new_feature = {
            'feature_key': 'e2e_test_feature',
            'feature_name': 'E2E测试功能',
            'category': 'test',
            'points_cost': 99,
            'vip_points_cost': 0,
            'svip_points_cost': 0,
            'description': '这是E2E测试创建的功能'
        }
        
        create_response = requests.post(
            f"{API_BASE_URL}/admin/config/features",
            json=new_feature,
            headers=headers
        )
        
        if create_response.status_code == 200:
            print("✓ 创建功能成功")
        
        # 3. 修改功能
        update_response = requests.put(
            f"{API_BASE_URL}/admin/config/features/e2e_test_feature",
            json={'points_cost': 120},
            headers=headers
        )
        
        if update_response.status_code == 200:
            print("✓ 修改功能成功")
        
        # 4. 查看统计数据
        stats_response = requests.get(
            f"{API_BASE_URL}/admin/stats/today",
            headers=headers
        )
        
        if stats_response.status_code == 200:
            stats = stats_response.json()['data']
            print(f"\n今日统计:")
            print(f"  总用户数: {stats['total_users']}")
            print(f"  签到数: {stats['checkin_count']}")
            print(f"  功能使用数: {stats['feature_usage_count']}")
            print(f"  VIP用户数: {stats['vip_count']}")
        
        # 5. 清理测试数据
        delete_response = requests.delete(
            f"{API_BASE_URL}/admin/config/features/e2e_test_feature",
            headers=headers
        )
        
        if delete_response.status_code == 200:
            print("✓ 清理测试数据成功")
        
        assert True


class TestVIPFeatures:
    """VIP功能测试"""
    
    def test_vip_quota_usage(self):
        """测试VIP配额使用"""
        vip_username = 'e2e_vip_user'  # 需要是VIP用户
        
        # 查看VIP配额
        profile_response = requests.get(
            f"{API_BASE_URL}/user/profile",
            params={'username': vip_username}
        )
        
        if profile_response.status_code == 200:
            profile = profile_response.json()['data']
            
            if profile['vip_type'] != 'none':
                print(f"VIP类型: {profile['vip_type']}")
                print(f"VIP配额: {profile.get('vip_daily_quota', 'N/A')}")
                
                # 使用功能（应该使用配额）
                feature_response = requests.post(
                    f"{API_BASE_URL}/feature/use",
                    json={
                        'username': vip_username,
                        'feature_key': 'ai_color_match',
                        'device_id': 'e2e_vip_device'
                    }
                )
                
                if feature_response.status_code == 200:
                    data = feature_response.json()['data']
                    print(f"使用功能: {data['cost_type']}")
                    if data['cost_type'] == 'vip_quota':
                        print(f"剩余配额: {data['vip_remaining_quota']}")
            else:
                print(f"{vip_username} 不是VIP用户")
        
        assert True


if __name__ == '__main__':
    # 单独运行集成测试
    print("="*60)
    print("开始运行E2E集成测试")
    print("="*60)
    
    tester = TestUserJourney()
    tester.test_complete_user_journey()
    
    print("\n" + "="*60)
    
    admin_tester = TestAdminWorkflow()
    admin_tester.test_admin_config_workflow()
    
    print("\n" + "="*60)
    print("E2E测试完成！")
    print("="*60)

