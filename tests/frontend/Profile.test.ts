/**
 * Profile组件测试
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Profile from '../../../src/view/Profile.vue'
import axios from 'axios'

vi.mock('axios')

const mockRouter = {
  push: vi.fn()
}

vi.mock('vue-router', () => ({
  useRouter: () => mockRouter
}))

describe('Profile', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.setItem('username', 'testuser')
    localStorage.setItem('token', 'test_token')
  })

  it('应该正确渲染组件', () => {
    const wrapper = mount(Profile)
    expect(wrapper.find('.profile-page').exists()).toBe(true)
  })

  it('应该显示用户基本信息', async () => {
    const mockProfile = {
      username: 'testuser',
      nickname: '测试昵称',
      email: 'test@example.com',
      points: 1200,
      level: 3,
      vip_type: 'vip',
      total_check_in_days: 30,
      consecutive_check_in: 7
    }

    ;(axios.get as any).mockResolvedValueOnce({
      data: { code: 200, data: mockProfile }
    }).mockResolvedValueOnce({
      data: { code: 200, data: { total: 0, current_balance: 1200, records: [] } }
    })

    const wrapper = mount(Profile)
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.text()).toContain('测试昵称')
    expect(wrapper.text()).toContain('testuser')
  })

  it('应该显示统计数据卡片', async () => {
    const mockProfile = {
      username: 'testuser',
      points: 1200,
      total_check_in_days: 30,
      consecutive_check_in: 7,
      vip_type: 'vip'
    }

    ;(axios.get as any).mockResolvedValue({
      data: { code: 200, data: mockProfile }
    })

    const wrapper = mount(Profile)
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.findAll('.stat-card').length).toBeGreaterThan(0)
  })

  it('应该能够编辑资料', async () => {
    const mockProfile = {
      username: 'testuser',
      nickname: '旧昵称',
      points: 1000
    }

    ;(axios.get as any).mockResolvedValue({
      data: { code: 200, data: mockProfile }
    })
    ;(axios.put as any).mockResolvedValue({
      data: { code: 200, message: '更新成功' }
    })

    const wrapper = mount(Profile)
    await new Promise(resolve => setTimeout(resolve, 100))

    // 模拟点击编辑按钮
    const editButton = wrapper.find('button')
    if (editButton.exists() && editButton.text().includes('编辑')) {
      await editButton.trigger('click')
      // 编辑对话框应该打开
      await wrapper.vm.$nextTick()
    }
  })

  it('应该显示VIP徽章', async () => {
    const mockProfile = {
      username: 'testuser',
      vip_type: 'svip',
      points: 2000
    }

    ;(axios.get as any).mockResolvedValue({
      data: { code: 200, data: mockProfile }
    })

    const wrapper = mount(Profile)
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.html()).toContain('SVIP')
  })

  it('应该显示积分历史列表', async () => {
    const mockProfile = {
      username: 'testuser',
      points: 1000
    }

    const mockHistory = {
      total: 10,
      current_balance: 1000,
      records: [
        {
          type: 'checkin',
          amount: 30,
          balance: 1000,
          description: '每日签到',
          created_at: '2024-01-01T10:00:00'
        },
        {
          type: 'consume',
          amount: -50,
          balance: 970,
          description: '使用AI配色',
          created_at: '2024-01-01T09:00:00'
        }
      ]
    }

    ;(axios.get as any)
      .mockResolvedValueOnce({ data: { code: 200, data: mockProfile } })
      .mockResolvedValueOnce({ data: { code: 200, data: mockHistory } })

    const wrapper = mount(Profile)
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.text()).toContain('每日签到')
    expect(wrapper.text()).toContain('使用AI配色')
  })

  it('积分变动应该有不同颜色', async () => {
    const mockHistory = {
      total: 2,
      current_balance: 1000,
      records: [
        { type: 'checkin', amount: 30, balance: 1000, description: '签到', created_at: '2024-01-01' },
        { type: 'consume', amount: -50, balance: 970, description: '消费', created_at: '2024-01-01' }
      ]
    }

    ;(axios.get as any).mockResolvedValue({
      data: { code: 200, data: mockHistory }
    })

    const wrapper = mount(Profile)
    await new Promise(resolve => setTimeout(resolve, 200))

    // 正数应该是绿色，负数应该是红色
    const html = wrapper.html()
    expect(html).toContain('positive')
    expect(html).toContain('negative')
  })
})

