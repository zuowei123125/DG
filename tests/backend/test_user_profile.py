# -*- coding: utf-8 -*-
"""
用户资料和积分历史API测试
"""

import pytest
import requests
from conftest import API_BASE_URL


class TestUserProfile:
    """用户资料测试"""
    
    def test_get_user_profile(self, test_user):
        """测试获取用户资料"""
        response = requests.get(
            f"{API_BASE_URL}/user/profile",
            params={'username': test_user['username']}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        data = result['data']
        assert data['username'] == test_user['username']
        assert 'points' in data
        assert 'vip_type' in data
        assert 'total_check_in_days' in data
        assert 'consecutive_check_in' in data
    
    def test_get_nonexistent_user_profile(self):
        """测试获取不存在的用户资料"""
        response = requests.get(
            f"{API_BASE_URL}/user/profile",
            params={'username': 'nonexistent_user'}
        )
        
        assert response.status_code == 404
    
    def test_update_user_profile(self, test_user):
        """测试更新用户资料"""
        update_data = {
            'username': test_user['username'],
            'nickname': '测试昵称',
            'email': 'newemail@test.com'
        }
        
        response = requests.put(
            f"{API_BASE_URL}/user/profile",
            json=update_data
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        assert result['message'] == '更新成功'
        
        # 验证更新
        profile_response = requests.get(
            f"{API_BASE_URL}/user/profile",
            params={'username': test_user['username']}
        )
        profile_data = profile_response.json()['data']
        assert profile_data['nickname'] == '测试昵称'
        assert profile_data['email'] == 'newemail@test.com'
    
    def test_update_partial_profile(self, test_user):
        """测试部分更新"""
        update_data = {
            'username': test_user['username'],
            'nickname': '仅更新昵称'
        }
        
        response = requests.put(
            f"{API_BASE_URL}/user/profile",
            json=update_data
        )
        
        assert response.status_code == 200
    
    def test_update_nonexistent_user_profile(self):
        """测试更新不存在的用户资料"""
        update_data = {
            'username': 'nonexistent_user',
            'nickname': '测试'
        }
        
        response = requests.put(
            f"{API_BASE_URL}/user/profile",
            json=update_data
        )
        
        assert response.status_code == 404


class TestPointsHistory:
    """积分历史测试"""
    
    def test_get_points_history(self, test_user):
        """测试获取积分历史"""
        response = requests.get(
            f"{API_BASE_URL}/points/history",
            params={'username': test_user['username'], 'page': 1, 'limit': 10}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        data = result['data']
        assert 'total' in data
        assert 'current_balance' in data
        assert 'records' in data
        assert isinstance(data['records'], list)
    
    def test_points_history_with_type_filter(self, test_user):
        """测试按类型筛选积分历史"""
        response = requests.get(
            f"{API_BASE_URL}/points/history",
            params={
                'username': test_user['username'],
                'type': 'checkin',
                'page': 1,
                'limit': 10
            }
        )
        
        assert response.status_code == 200
        data = response.json()['data']
        
        # 验证所有记录都是签到类型
        for record in data['records']:
            assert record['type'] == 'checkin'
    
    def test_points_history_pagination(self, test_user):
        """测试分页"""
        response = requests.get(
            f"{API_BASE_URL}/points/history",
            params={'username': test_user['username'], 'page': 1, 'limit': 5}
        )
        
        assert response.status_code == 200
        data = response.json()['data']
        assert len(data['records']) <= 5
    
    def test_points_history_structure(self, test_user, db_cursor):
        """测试记录结构"""
        # 创建一条测试记录
        db_cursor.execute("""
            INSERT INTO points_history 
            (user_id, username, type, amount, balance, description)
            VALUES (%s, %s, 'reward', 50, 150, '测试奖励')
        """, (test_user['id'], test_user['username']))
        db_cursor.connection.commit()
        
        response = requests.get(
            f"{API_BASE_URL}/points/history",
            params={'username': test_user['username']}
        )
        
        data = response.json()['data']
        if len(data['records']) > 0:
            record = data['records'][0]
            assert 'type' in record
            assert 'amount' in record
            assert 'balance' in record
            assert 'description' in record
            assert 'created_at' in record
    
    def test_points_history_after_checkin(self, test_user):
        """测试签到后积分历史增加"""
        # 获取签到前记录数
        response_before = requests.get(
            f"{API_BASE_URL}/points/history",
            params={'username': test_user['username']}
        )
        total_before = response_before.json()['data']['total']
        
        # 签到
        requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': test_user['username']}
        )
        
        # 获取签到后记录数
        response_after = requests.get(
            f"{API_BASE_URL}/points/history",
            params={'username': test_user['username']}
        )
        total_after = response_after.json()['data']['total']
        
        # 签到会增加一条积分历史
        assert total_after == total_before + 1
    
    def test_points_history_nonexistent_user(self):
        """测试不存在的用户的积分历史"""
        response = requests.get(
            f"{API_BASE_URL}/points/history",
            params={'username': 'nonexistent_user'}
        )
        
        assert response.status_code == 404


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

