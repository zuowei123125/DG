/**
 * HomePage组件测试
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import HomePage from '../../../src/view/HomePage.vue'
import { Message } from '@arco-design/web-vue'
import axios from 'axios'

// Mock axios
vi.mock('axios')

// Mock Arco Design Message
vi.mock('@arco-design/web-vue', () => ({
  Message: {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn()
  }
}))

// Mock router
const mockRouter = {
  push: vi.fn()
}

vi.mock('vue-router', () => ({
  useRouter: () => mockRouter
}))

describe('HomePage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.setItem('username', 'testuser')
    localStorage.setItem('token', 'test_token')
  })

  it('应该正确渲染组件', () => {
    const wrapper = mount(HomePage)
    expect(wrapper.find('.home-page').exists()).toBe(true)
  })

  it('应该显示欢迎信息', async () => {
    // Mock API响应
    const mockUserInfo = {
      username: 'testuser',
      nickname: '测试用户',
      points: 1000,
      vip_type: 'vip',
      consecutive_check_in: 7
    }

    ;(axios.get as any).mockResolvedValueOnce({
      data: {
        code: 200,
        data: mockUserInfo
      }
    })

    const wrapper = mount(HomePage)
    await wrapper.vm.$nextTick()

    // 等待数据加载
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.text()).toContain('测试用户')
  })

  it('应该显示正确的积分数量', async () => {
    const mockUserInfo = {
      username: 'testuser',
      points: 1500,
      vip_type: 'none',
      consecutive_check_in: 3
    }

    ;(axios.get as any).mockResolvedValueOnce({
      data: {
        code: 200,
        data: mockUserInfo
      }
    })

    const wrapper = mount(HomePage)
    await new Promise(resolve => setTimeout(resolve, 100))

    // 应该显示1500积分
    expect(wrapper.html()).toContain('1500')
  })

  it('应该显示VIP状态', async () => {
    const mockUserInfo = {
      username: 'testuser',
      points: 1000,
      vip_type: 'svip',
      consecutive_check_in: 10
    }

    ;(axios.get as any).mockResolvedValueOnce({
      data: {
        code: 200,
        data: mockUserInfo
      }
    })

    const wrapper = mount(HomePage)
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.text()).toContain('SVIP')
  })

  it('点击功能卡片应该调用使用功能API', async () => {
    const mockUserInfo = {
      username: 'testuser',
      points: 1000,
      vip_type: 'none',
      consecutive_check_in: 5
    }

    const mockFeatureResponse = {
      data: {
        code: 200,
        data: {
          success: true,
          cost_type: 'points',
          points_cost: 50,
          points_remaining: 950,
          message: '使用成功'
        }
      }
    }

    ;(axios.get as any).mockResolvedValueOnce({
      data: { code: 200, data: mockUserInfo }
    })
    ;(axios.post as any).mockResolvedValueOnce(mockFeatureResponse)

    const wrapper = mount(HomePage)
    await new Promise(resolve => setTimeout(resolve, 100))

    // 模拟点击功能卡片
    const featureItem = wrapper.find('.feature-item')
    if (featureItem.exists()) {
      await featureItem.trigger('click')
      
      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/feature/use'),
        expect.objectContaining({
          username: 'testuser',
          feature_key: expect.any(String),
          device_id: expect.any(String)
        })
      )
    }
  })

  it('积分不足时应该显示错误提示', async () => {
    const mockUserInfo = {
      username: 'testuser',
      points: 10,
      vip_type: 'none',
      consecutive_check_in: 1
    }

    ;(axios.get as any).mockResolvedValueOnce({
      data: { code: 200, data: mockUserInfo }
    })
    ;(axios.post as any).mockRejectedValueOnce({
      response: {
        data: {
          detail: '积分不足'
        }
      }
    })

    const wrapper = mount(HomePage)
    await new Promise(resolve => setTimeout(resolve, 100))

    const featureItem = wrapper.find('.feature-item')
    if (featureItem.exists()) {
      await featureItem.trigger('click')
      await new Promise(resolve => setTimeout(resolve, 100))
      
      expect(Message.error).toHaveBeenCalled()
    }
  })

  it('应该有快捷入口按钮', async () => {
    const wrapper = mount(HomePage)
    
    expect(wrapper.text()).toContain('每日签到')
    expect(wrapper.text()).toContain('个人中心')
    expect(wrapper.text()).toContain('工作台')
  })

  it('未登录时应该跳转到登录页', async () => {
    localStorage.removeItem('username')
    localStorage.removeItem('token')

    ;(axios.get as any).mockRejectedValueOnce(new Error('Unauthorized'))

    const wrapper = mount(HomePage)
    await new Promise(resolve => setTimeout(resolve, 100))

    // 应该尝试跳转到登录页
    expect(mockRouter.push).toHaveBeenCalledWith('/login')
  })
})

