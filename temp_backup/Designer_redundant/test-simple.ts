/**
 * 超级简单的测试 - 验证最基础的 evalScript
 */

import { cep } from "@/utils/cep";

/**
 * 测试1：最简单的计算
 */
export async function testSimpleCalc() {
    try {
        const result = await cep.evalScript("1 + 2 + 3");
        console.log('简单计算结果:', result);
        return { success: true, result };
    } catch (error) {
        console.error('简单计算失败:', error);
        return { success: false, error: String(error) };
    }
}

/**
 * 测试2：获取应用名称（不依赖任何工具库）
 */
export async function testGetAppName() {
    try {
        const result = await cep.evalScript("app.name");
        console.log('应用名称:', result);
        return { success: true, appName: result };
    } catch (error) {
        console.error('获取应用名称失败:', error);
        return { success: false, error: String(error) };
    }
}

/**
 * 测试3：创建图层（最简单版本，不依赖工具库）
 */
export async function testCreateLayerDirect() {
    const jsx = `
        (function() {
            try {
                if (app.documents.length === 0) {
                    return "no_document";
                }
                var doc = app.activeDocument;
                var layer = doc.artLayers.add();
                layer.name = "TestLayer";
                return "success:" + layer.name;
            } catch (e) {
                return "error:" + e.toString();
            }
        })()
    `;
    
    try {
        const result = await cep.evalScript(jsx);
        console.log('创建图层结果:', result);
        return { success: true, result };
    } catch (error) {
        console.error('创建图层失败:', error);
        return { success: false, error: String(error) };
    }
}

