# -*- coding: utf-8 -*-
"""
管理员配置API测试
测试功能配置、VIP配置、签到配置的CRUD操作
"""

import pytest
import requests
from conftest import API_BASE_URL, ADMIN_TOKEN


class TestFeaturesConfig:
    """功能配置测试"""
    
    def test_get_features_config(self, admin_headers):
        """测试获取功能配置列表"""
        response = requests.get(
            f"{API_BASE_URL}/admin/config/features",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # 验证数据结构
        feature = data[0]
        assert 'feature_key' in feature
        assert 'feature_name' in feature
        assert 'points_cost' in feature
        assert 'enabled' in feature
    
    def test_create_feature_config(self, admin_headers):
        """测试创建功能配置"""
        feature_data = {
            'feature_key': 'test_feature_api',
            'feature_name': 'API测试功能',
            'category': 'test',
            'points_cost': 60,
            'vip_points_cost': 0,
            'svip_points_cost': 0,
            'description': '这是一个API测试功能'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/admin/config/features",
            json=feature_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        assert result['message'] == '创建成功'
        
        # 清理
        requests.delete(
            f"{API_BASE_URL}/admin/config/features/test_feature_api",
            headers=admin_headers
        )
    
    def test_update_feature_config(self, admin_headers, test_feature):
        """测试更新功能配置"""
        feature_key = test_feature['feature_key']
        
        update_data = {
            'points_cost': 80,
            'enabled': True
        }
        
        response = requests.put(
            f"{API_BASE_URL}/admin/config/features/{feature_key}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
    
    def test_update_nonexistent_feature(self, admin_headers):
        """测试更新不存在的功能"""
        response = requests.put(
            f"{API_BASE_URL}/admin/config/features/nonexistent_feature",
            json={'points_cost': 100},
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_feature_config(self, admin_headers):
        """测试删除功能配置"""
        # 先创建
        feature_key = 'test_delete_feature'
        requests.post(
            f"{API_BASE_URL}/admin/config/features",
            json={
                'feature_key': feature_key,
                'feature_name': '待删除功能',
                'category': 'test',
                'points_cost': 50,
                'vip_points_cost': 0,
                'svip_points_cost': 0
            },
            headers=admin_headers
        )
        
        # 删除
        response = requests.delete(
            f"{API_BASE_URL}/admin/config/features/{feature_key}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200


class TestVIPConfig:
    """VIP配置测试"""
    
    def test_get_vip_config(self, admin_headers):
        """测试获取VIP配置"""
        response = requests.get(
            f"{API_BASE_URL}/admin/config/vip",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2  # VIP和SVIP
        
        # 验证数据结构
        vip = next((v for v in data if v['vip_type'] == 'vip'), None)
        assert vip is not None
        assert 'price' in vip
        assert 'daily_quota' in vip
        assert 'points_multiplier' in vip
    
    def test_update_vip_config(self, admin_headers):
        """测试更新VIP配置"""
        update_data = {
            'price': 35.00,
            'daily_quota': 25
        }
        
        response = requests.put(
            f"{API_BASE_URL}/admin/config/vip/vip",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        # 恢复原值
        requests.put(
            f"{API_BASE_URL}/admin/config/vip/vip",
            json={'price': 30.00, 'daily_quota': 20},
            headers=admin_headers
        )
    
    def test_update_invalid_vip_type(self, admin_headers):
        """测试更新无效的VIP类型"""
        response = requests.put(
            f"{API_BASE_URL}/admin/config/vip/invalid",
            json={'price': 100},
            headers=admin_headers
        )
        
        assert response.status_code == 400


class TestCheckInConfig:
    """签到配置测试"""
    
    def test_get_checkin_config(self, admin_headers):
        """测试获取签到配置"""
        response = requests.get(
            f"{API_BASE_URL}/admin/config/checkin",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # 验证数据结构
        config = data[0]
        assert 'consecutive_days' in config
        assert 'base_points' in config
        assert 'bonus_points' in config
        assert 'total_points' in config
    
    def test_create_checkin_config(self, admin_headers):
        """测试创建签到档位"""
        config_data = {
            'consecutive_days': 99,
            'base_points': 10,
            'bonus_points': 200,
            'total_points': 210
        }
        
        response = requests.post(
            f"{API_BASE_URL}/admin/config/checkin",
            json=config_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        # 清理
        requests.delete(
            f"{API_BASE_URL}/admin/config/checkin/99",
            headers=admin_headers
        )
    
    def test_update_checkin_config(self, admin_headers):
        """测试更新签到档位"""
        # 假设第7天的配置存在
        update_data = {
            'bonus_points': 25,
            'total_points': 35
        }
        
        response = requests.put(
            f"{API_BASE_URL}/admin/config/checkin/7",
            json=update_data,
            headers=admin_headers
        )
        
        # 可能成功也可能404（取决于是否存在）
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            # 恢复原值
            requests.put(
                f"{API_BASE_URL}/admin/config/checkin/7",
                json={'bonus_points': 20, 'total_points': 30},
                headers=admin_headers
            )
    
    def test_delete_checkin_config(self, admin_headers):
        """测试删除签到档位"""
        # 先创建
        requests.post(
            f"{API_BASE_URL}/admin/config/checkin",
            json={
                'consecutive_days': 88,
                'base_points': 10,
                'bonus_points': 150,
                'total_points': 160
            },
            headers=admin_headers
        )
        
        # 删除
        response = requests.delete(
            f"{API_BASE_URL}/admin/config/checkin/88",
            headers=admin_headers
        )
        
        assert response.status_code in [200, 404]


class TestAdminAuth:
    """管理员权限测试"""
    
    def test_unauthorized_access(self):
        """测试未授权访问"""
        response = requests.get(
            f"{API_BASE_URL}/admin/config/features",
            headers={'x-admin-token': 'invalid_token'}
        )
        
        assert response.status_code == 401
    
    def test_missing_token(self):
        """测试缺少token"""
        response = requests.get(
            f"{API_BASE_URL}/admin/config/features"
        )
        
        assert response.status_code in [401, 422]  # FastAPI可能返回422


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

