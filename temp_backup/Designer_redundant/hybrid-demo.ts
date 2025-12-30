/**
 * 混合方案 Demo - 简单版
 * 前端获取图层名称 → 后端计算 → 前端显示结果
 */

import { evalInlineJSX, JSXResponse } from './utils';
import { config } from '@/config';

/**
 * Demo：获取当前图层名称并计算
 * 
 * 流程：
 * 1. 本地 → 获取当前图层名称（如 "87-98"）
 * 2. 本地 → 发送到服务器
 * 3. 服务器 → 计算数学表达式（核心算法）
 * 4. 服务器 → 返回计算结果
 * 5. 本地 → 显示结果
 */
export async function calculateLayerName(): Promise<JSXResponse> {
    try {
        // 1. 💻 本地获取图层名称（简单 JSX）
        const jsx = `
            try {
                if (!$.global.JSXUtils.hasDocument()) {
                    return $.global.JSXUtils.stringify({ error: '没有打开的文档' });
                }
                
                var doc = $.global.JSXUtils.getDocument();
                
                if (doc.activeLayer) {
                    return $.global.JSXUtils.stringify({ 
                        success: true,
                        layerName: doc.activeLayer.name
                    });
                } else {
                    return $.global.JSXUtils.stringify({ 
                        error: '没有选中的图层'
                    });
                }
            } catch (error) {
                return $.global.JSXUtils.stringify({ 
                    error: error.toString() 
                });
            }
        `;
        
        const layerResult = await evalInlineJSX(jsx);
        
        if (layerResult.error || !layerResult.success) {
            return layerResult;
        }
        
        const layerName = layerResult.layerName;
        
        // 2. 🌐 发送到服务器计算（核心算法在服务器，使用 API Key 验证）
        const response = await fetch(`${config.apiBaseUrl}/jsx_demo/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': 'demo_key_123'  // 🔐 API Key 验证
            },
            body: JSON.stringify({
                expression: layerName
            })
        });
        
        if (!response.ok) {
            return { error: '服务器错误' };
        }
        
        const calcResult = await response.json();
        
        return {
            success: calcResult.success,
            expression: calcResult.expression,
            result: calcResult.result,
            message: calcResult.message,
            layerName: layerName
        };
        
    } catch (error) {
        return { error: String(error) };
    }
}
