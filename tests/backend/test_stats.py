# -*- coding: utf-8 -*-
"""
统计API测试
测试数据统计功能
"""

import pytest
import requests
from conftest import API_BASE_URL, ADMIN_TOKEN


class TestTodayStats:
    """今日统计测试"""
    
    def test_get_today_stats(self, admin_headers):
        """测试获取今日统计"""
        response = requests.get(
            f"{API_BASE_URL}/admin/stats/today",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        data = result['data']
        assert 'total_users' in data
        assert 'checkin_count' in data
        assert 'feature_usage_count' in data
        assert 'vip_count' in data
        
        # 验证数据类型
        assert isinstance(data['total_users'], int)
        assert isinstance(data['checkin_count'], int)
        assert isinstance(data['feature_usage_count'], int)
        assert isinstance(data['vip_count'], int)
        
        # 验证数据合理性
        assert data['total_users'] >= 0
        assert data['checkin_count'] >= 0
        assert data['checkin_count'] <= data['total_users']
    
    def test_stats_unauthorized(self):
        """测试未授权访问统计"""
        response = requests.get(f"{API_BASE_URL}/admin/stats/today")
        
        assert response.status_code in [401, 422]


class TestFeatureUsageStats:
    """功能使用排行测试"""
    
    def test_get_feature_usage_stats(self, admin_headers):
        """测试获取功能使用排行"""
        response = requests.get(
            f"{API_BASE_URL}/admin/stats/feature-usage",
            params={'days': 7},
            headers=admin_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        data = result['data']
        assert isinstance(data, list)
        
        # 如果有数据，验证结构
        if len(data) > 0:
            item = data[0]
            assert 'feature_key' in item
            assert 'feature_name' in item
            assert 'usage_count' in item
            assert isinstance(item['usage_count'], int)
    
    def test_feature_usage_stats_different_days(self, admin_headers):
        """测试不同天数的统计"""
        days_list = [7, 30, 90]
        
        for days in days_list:
            response = requests.get(
                f"{API_BASE_URL}/admin/stats/feature-usage",
                params={'days': days},
                headers=admin_headers
            )
            
            assert response.status_code == 200
            assert response.json()['code'] == 200


class TestPointsTrend:
    """积分趋势测试"""
    
    def test_get_points_trend(self, admin_headers):
        """测试获取积分趋势"""
        response = requests.get(
            f"{API_BASE_URL}/admin/stats/points-trend",
            params={'days': 7},
            headers=admin_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        data = result['data']
        assert isinstance(data, list)
        
        # 如果有数据，验证结构
        if len(data) > 0:
            item = data[0]
            assert 'date' in item
            assert 'earned' in item
            assert 'consumed' in item
            
            # 验证数据类型
            assert isinstance(item['earned'], (int, float, type(None)))
            assert isinstance(item['consumed'], (int, float, type(None)))
    
    def test_points_trend_date_format(self, admin_headers):
        """测试日期格式"""
        response = requests.get(
            f"{API_BASE_URL}/admin/stats/points-trend",
            params={'days': 7},
            headers=admin_headers
        )
        
        data = response.json()['data']
        
        if len(data) > 0:
            # 验证日期格式 (YYYY-MM-DD)
            import re
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            assert re.match(date_pattern, data[0]['date'])


class TestStatsIntegration:
    """统计集成测试"""
    
    def test_stats_after_operations(self, test_user, test_feature, admin_headers, db_cursor):
        """测试操作后统计数据变化"""
        # 获取操作前统计
        response_before = requests.get(
            f"{API_BASE_URL}/admin/stats/today",
            headers=admin_headers
        )
        stats_before = response_before.json()['data']
        
        # 执行签到
        requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': test_user['username']}
        )
        
        # 使用功能
        requests.post(
            f"{API_BASE_URL}/feature/use",
            json={
                'username': test_user['username'],
                'feature_key': test_feature['feature_key'],
                'device_id': 'test'
            }
        )
        
        # 获取操作后统计
        response_after = requests.get(
            f"{API_BASE_URL}/admin/stats/today",
            headers=admin_headers
        )
        stats_after = response_after.json()['data']
        
        # 验证签到数增加
        assert stats_after['checkin_count'] >= stats_before['checkin_count']
        
        # 验证功能使用数增加
        assert stats_after['feature_usage_count'] >= stats_before['feature_usage_count']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

