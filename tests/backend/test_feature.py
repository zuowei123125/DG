# -*- coding: utf-8 -*-
"""
功能使用API测试
测试核心扣费逻辑、VIP配额管理
"""

import pytest
import requests
from conftest import API_BASE_URL


class TestFeatureUsage:
    """功能使用测试"""
    
    def test_use_feature_normal_user(self, test_user, test_feature):
        """测试普通用户使用功能（扣积分）"""
        request_data = {
            'username': test_user['username'],
            'feature_key': test_feature['feature_key'],
            'device_id': 'test_device'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/feature/use",
            json=request_data
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        data = result['data']
        assert data['success'] is True
        assert data['cost_type'] == 'points'
        assert data['points_cost'] == test_feature['points_cost']
        assert data['points_remaining'] == test_user['points'] - test_feature['points_cost']
    
    def test_use_feature_insufficient_points(self, test_user, test_feature, db_cursor):
        """测试积分不足"""
        # 设置用户积分为0
        db_cursor.execute(
            "UPDATE users SET points = 0 WHERE username = %s",
            (test_user['username'],)
        )
        db_cursor.connection.commit()
        
        request_data = {
            'username': test_user['username'],
            'feature_key': test_feature['feature_key'],
            'device_id': 'test_device'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/feature/use",
            json=request_data
        )
        
        assert response.status_code == 402
        assert '积分不足' in response.json()['detail']
    
    def test_use_feature_vip_user_with_quota(self, vip_user, test_feature):
        """测试VIP用户使用配额"""
        request_data = {
            'username': vip_user['username'],
            'feature_key': test_feature['feature_key'],
            'device_id': 'test_device'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/feature/use",
            json=request_data
        )
        
        assert response.status_code == 200
        result = response.json()
        
        data = result['data']
        # VIP用户应该使用配额（如果vip_points_cost=0）
        assert data['cost_type'] in ['vip_quota', 'points']
        
        if data['cost_type'] == 'vip_quota':
            assert data['vip_remaining_quota'] == vip_user['vip_daily_quota'] - 1
    
    def test_use_disabled_feature(self, test_user, test_feature, db_cursor):
        """测试使用已禁用的功能"""
        # 禁用功能
        db_cursor.execute(
            "UPDATE features_config SET enabled = 0 WHERE feature_key = %s",
            (test_feature['feature_key'],)
        )
        db_cursor.connection.commit()
        
        request_data = {
            'username': test_user['username'],
            'feature_key': test_feature['feature_key'],
            'device_id': 'test_device'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/feature/use",
            json=request_data
        )
        
        assert response.status_code == 400
        assert '禁用' in response.json()['detail']
        
        # 恢复
        db_cursor.execute(
            "UPDATE features_config SET enabled = 1 WHERE feature_key = %s",
            (test_feature['feature_key'],)
        )
        db_cursor.connection.commit()
    
    def test_use_nonexistent_feature(self, test_user):
        """测试使用不存在的功能"""
        request_data = {
            'username': test_user['username'],
            'feature_key': 'nonexistent_feature',
            'device_id': 'test_device'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/feature/use",
            json=request_data
        )
        
        assert response.status_code == 400
    
    def test_use_feature_nonexistent_user(self, test_feature):
        """测试不存在的用户使用功能"""
        request_data = {
            'username': 'nonexistent_user',
            'feature_key': test_feature['feature_key'],
            'device_id': 'test_device'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/feature/use",
            json=request_data
        )
        
        assert response.status_code == 404


class TestFeatureUsageLogging:
    """功能使用日志测试"""
    
    def test_usage_log_created(self, test_user, test_feature, db_cursor):
        """测试使用后创建日志"""
        # 使用前记录数
        db_cursor.execute(
            "SELECT COUNT(*) as count FROM feature_usage_logs WHERE username = %s",
            (test_user['username'],)
        )
        count_before = db_cursor.fetchone()['count']
        
        # 使用功能
        request_data = {
            'username': test_user['username'],
            'feature_key': test_feature['feature_key'],
            'device_id': 'test_device'
        }
        
        requests.post(f"{API_BASE_URL}/feature/use", json=request_data)
        
        # 使用后记录数
        db_cursor.execute(
            "SELECT COUNT(*) as count FROM feature_usage_logs WHERE username = %s",
            (test_user['username'],)
        )
        count_after = db_cursor.fetchone()['count']
        
        assert count_after == count_before + 1
    
    def test_points_history_created(self, test_user, test_feature, db_cursor):
        """测试积分历史记录"""
        # 使用前记录数
        db_cursor.execute(
            "SELECT COUNT(*) as count FROM points_history WHERE username = %s",
            (test_user['username'],)
        )
        count_before = db_cursor.fetchone()['count']
        
        # 使用功能
        request_data = {
            'username': test_user['username'],
            'feature_key': test_feature['feature_key'],
            'device_id': 'test_device'
        }
        
        response = requests.post(f"{API_BASE_URL}/feature/use", json=request_data)
        
        # 只有扣积分时才记录积分历史
        if response.status_code == 200:
            data = response.json()['data']
            if data['cost_type'] == 'points':
                db_cursor.execute(
                    "SELECT COUNT(*) as count FROM points_history WHERE username = %s",
                    (test_user['username'],)
                )
                count_after = db_cursor.fetchone()['count']
                assert count_after == count_before + 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

