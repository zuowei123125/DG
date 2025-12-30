# -*- coding: utf-8 -*-
"""
签到API测试
测试签到功能、连续天数计算、VIP倍数
"""

import pytest
import requests
from datetime import date
from conftest import API_BASE_URL


class TestDailyCheckIn:
    """每日签到测试"""
    
    def test_first_checkin(self, test_user):
        """测试首次签到"""
        request_data = {'username': test_user['username']}
        
        response = requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json=request_data
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        data = result['data']
        assert data['success'] is True
        assert data['consecutive_days'] == 1
        assert data['points_earned'] > 0
        assert '签到成功' in data['message']
    
    def test_duplicate_checkin(self, test_user, db_cursor):
        """测试重复签到"""
        # 先签到一次
        requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': test_user['username']}
        )
        
        # 再次签到
        response = requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': test_user['username']}
        )
        
        assert response.status_code == 400
        assert '已签到' in response.json()['detail']
    
    def test_consecutive_checkin_calculation(self, test_user, db_cursor):
        """测试连续天数计算"""
        from datetime import timedelta
        
        # 设置昨天签到
        yesterday = date.today() - timedelta(days=1)
        db_cursor.execute("""
            UPDATE users 
            SET last_check_in_date = %s, consecutive_check_in = 5
            WHERE username = %s
        """, (yesterday, test_user['username']))
        db_cursor.connection.commit()
        
        # 今天签到
        response = requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': test_user['username']}
        )
        
        assert response.status_code == 200
        data = response.json()['data']
        
        # 连续天数应该+1
        assert data['consecutive_days'] == 6
    
    def test_broken_consecutive_checkin(self, test_user, db_cursor):
        """测试中断连续签到"""
        from datetime import timedelta
        
        # 设置3天前签到
        three_days_ago = date.today() - timedelta(days=3)
        db_cursor.execute("""
            UPDATE users 
            SET last_check_in_date = %s, consecutive_check_in = 10
            WHERE username = %s
        """, (three_days_ago, test_user['username']))
        db_cursor.connection.commit()
        
        # 今天签到
        response = requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': test_user['username']}
        )
        
        assert response.status_code == 200
        data = response.json()['data']
        
        # 连续天数应该归零重新开始
        assert data['consecutive_days'] == 1
    
    def test_vip_multiplier(self, vip_user):
        """测试VIP倍数"""
        response = requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': vip_user['username']}
        )
        
        assert response.status_code == 200
        data = response.json()['data']
        
        # VIP应该有倍数
        assert data['vip_multiplier'] >= 1.0
        if vip_user['vip_type'] == 'vip':
            assert data['vip_multiplier'] == 1.5
    
    def test_checkin_nonexistent_user(self):
        """测试不存在的用户签到"""
        response = requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': 'nonexistent_user'}
        )
        
        assert response.status_code == 404


class TestCheckInStatus:
    """签到状态测试"""
    
    def test_get_checkin_status(self, test_user):
        """测试获取签到状态"""
        response = requests.get(
            f"{API_BASE_URL}/checkin/status",
            params={'username': test_user['username']}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        data = result['data']
        assert 'today_checked' in data
        assert 'consecutive_days' in data
        assert 'total_days' in data
    
    def test_status_after_checkin(self, test_user):
        """测试签到后状态更新"""
        # 签到
        requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': test_user['username']}
        )
        
        # 查询状态
        response = requests.get(
            f"{API_BASE_URL}/checkin/status",
            params={'username': test_user['username']}
        )
        
        data = response.json()['data']
        assert data['today_checked'] is True


class TestCheckInCalendar:
    """签到日历测试"""
    
    def test_get_checkin_calendar(self, test_user):
        """测试获取签到日历"""
        today = date.today()
        
        response = requests.get(
            f"{API_BASE_URL}/checkin/calendar/{today.year}/{today.month}",
            params={'username': test_user['username']}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        data = result['data']
        assert data['year'] == today.year
        assert data['month'] == today.month
        assert isinstance(data['checked_dates'], list)
    
    def test_calendar_after_checkin(self, test_user, db_cursor):
        """测试签到后日历更新"""
        today = date.today()
        
        # 签到
        requests.post(
            f"{API_BASE_URL}/checkin/daily",
            json={'username': test_user['username']}
        )
        
        # 查询日历
        response = requests.get(
            f"{API_BASE_URL}/checkin/calendar/{today.year}/{today.month}",
            params={'username': test_user['username']}
        )
        
        data = response.json()['data']
        assert today.day in data['checked_dates']


class TestCheckInHistory:
    """签到历史测试"""
    
    def test_get_checkin_history(self, test_user):
        """测试获取签到历史"""
        response = requests.get(
            f"{API_BASE_URL}/checkin/history",
            params={'username': test_user['username'], 'page': 1, 'limit': 10}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        
        data = result['data']
        assert 'total' in data
        assert 'records' in data
        assert isinstance(data['records'], list)
    
    def test_history_after_checkin(self, test_user):
        """测试签到后历史记录增加"""
        # 获取签到前记录数
        response_before = requests.get(
            f"{API_BASE_URL}/checkin/history",
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
            f"{API_BASE_URL}/checkin/history",
            params={'username': test_user['username']}
        )
        total_after = response_after.json()['data']['total']
        
        assert total_after == total_before + 1
    
    def test_history_pagination(self, test_user):
        """测试分页"""
        response = requests.get(
            f"{API_BASE_URL}/checkin/history",
            params={'username': test_user['username'], 'page': 1, 'limit': 5}
        )
        
        assert response.status_code == 200
        data = response.json()['data']
        assert len(data['records']) <= 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

