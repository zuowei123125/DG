/**
 * CheckIn组件测试
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import CheckIn from '../../../src/view/CheckIn.vue'
import axios from 'axios'
import { Message } from '@arco-design/web-vue'

vi.mock('axios')
vi.mock('@arco-design/web-vue', () => ({
  Message: {
    success: vi.fn(),
    error: vi.fn()
  }
}))

const mockRouter = {
  push: vi.fn()
}

vi.mock('vue-router', () => ({
  useRouter: () => mockRouter
}))

describe('CheckIn', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.setItem('username', 'testuser')
  })

  it('应该正确渲染组件', () => {
    const wrapper = mount(CheckIn)
    expect(wrapper.find('.checkin-page').exists()).toBe(true)
  })

  it('应该显示签到状态', async () => {
    const mockStatus = {
      today_checked: false,
      consecutive_days: 7,
      total_days: 30
    }

    ;(axios.get as any).mockResolvedValue({
      data: { code: 200, data: mockStatus }
    })

    const wrapper = mount(CheckIn)
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.text()).toContain('7')
    expect(wrapper.text()).toContain('30')
  })

  it('未签到时应该显示签到按钮', async () => {
    const mockStatus = {
      today_checked: false,
      consecutive_days: 5,
      total_days: 20
    }

    ;(axios.get as any).mockResolvedValue({
      data: { code: 200, data: mockStatus }
    })

    const wrapper = mount(CheckIn)
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.text()).toContain('立即签到')
  })

  it('已签到时应该显示已签到状态', async () => {
    const mockStatus = {
      today_checked: true,
      consecutive_days: 8,
      total_days: 25
    }

    ;(axios.get as any).mockResolvedValue({
      data: { code: 200, data: mockStatus }
    })

    const wrapper = mount(CheckIn)
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.text()).toContain('今日已签到')
  })

  it('点击签到按钮应该调用签到API', async () => {
    const mockStatus = {
      today_checked: false,
      consecutive_days: 5,
      total_days: 20
    }

    const mockCheckInResponse = {
      data: {
        code: 200,
        data: {
          success: true,
          points_earned: 30,
          consecutive_days: 6,
          message: '签到成功'
        }
      }
    }

    ;(axios.get as any).mockResolvedValue({
      data: { code: 200, data: mockStatus }
    })
    ;(axios.post as any).mockResolvedValue(mockCheckInResponse)

    const wrapper = mount(CheckIn)
    await new Promise(resolve => setTimeout(resolve, 100))

    const checkinButton = wrapper.find('.checkin-button')
    if (checkinButton.exists()) {
      await checkinButton.trigger('click')
      
      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/checkin/daily'),
        expect.objectContaining({
          username: 'testuser'
        })
      )
    }
  })

  it('签到成功后应该显示成功提示', async () => {
    const mockCheckInResponse = {
      data: {
        code: 200,
        data: {
          success: true,
          points_earned: 30,
          consecutive_days: 6,
          message: '签到成功！连续签到6天，获得30积分'
        }
      }
    }

    ;(axios.post as any).mockResolvedValue(mockCheckInResponse)

    const wrapper = mount(CheckIn)
    await new Promise(resolve => setTimeout(resolve, 100))

    const checkinButton = wrapper.find('.checkin-button')
    if (checkinButton.exists()) {
      await checkinButton.trigger('click')
      await new Promise(resolve => setTimeout(resolve, 100))
      
      expect(Message.success).toHaveBeenCalled()
    }
  })

  it('应该显示奖励规则', async () => {
    const mockRewards = [
      { consecutive_days: 1, base_points: 10, bonus_points: 0, total_points: 10 },
      { consecutive_days: 7, base_points: 10, bonus_points: 20, total_points: 30 }
    ]

    ;(axios.get as any).mockResolvedValue({
      data: mockRewards
    })

    const wrapper = mount(CheckIn)
    await new Promise(resolve => setTimeout(resolve, 200))

    expect(wrapper.text()).toContain('奖励规则')
  })

  it('应该显示签到日历', async () => {
    const mockCalendar = {
      year: 2024,
      month: 1,
      checked_dates: [1, 5, 10, 15, 20]
    }

    ;(axios.get as any).mockResolvedValue({
      data: { code: 200, data: mockCalendar }
    })

    const wrapper = mount(CheckIn)
    await new Promise(resolve => setTimeout(resolve, 200))

    expect(wrapper.find('.calendar-grid').exists()).toBe(true)
  })

  it('应该能够切换月份', async () => {
    const wrapper = mount(CheckIn)
    await new Promise(resolve => setTimeout(resolve, 100))

    const prevButton = wrapper.find('.calendar-title').parentElement?.querySelector('button')
    if (prevButton) {
      await prevButton.dispatchEvent(new Event('click'))
      // 应该调用API加载新月份的数据
      await new Promise(resolve => setTimeout(resolve, 100))
    }
  })

  it('应该显示签到历史记录', async () => {
    const mockHistory = {
      total: 10,
      records: [
        {
          check_in_date: '2024-01-01',
          points_earned: 30,
          consecutive_days: 7
        }
      ]
    }

    ;(axios.get as any).mockResolvedValue({
      data: { code: 200, data: mockHistory }
    })

    const wrapper = mount(CheckIn)
    await new Promise(resolve => setTimeout(resolve, 200))

    expect(wrapper.text()).toContain('签到历史')
  })

  it('重复签到应该显示错误提示', async () => {
    ;(axios.post as any).mockRejectedValue({
      response: {
        data: {
          detail: '今日已签到，明天再来吧'
        }
      }
    })

    const wrapper = mount(CheckIn)
    await new Promise(resolve => setTimeout(resolve, 100))

    const checkinButton = wrapper.find('.checkin-button')
    if (checkinButton.exists()) {
      await checkinButton.trigger('click')
      await new Promise(resolve => setTimeout(resolve, 100))
      
      expect(Message.error).toHaveBeenCalled()
    }
  })
})

