import { copyCepToDev, copyCepToProd } from "./copyCepToDev"
import { createConfig } from "./createConfig"
// 注意：已移除 buildJsx 依赖，现在使用内联 JSX 方式
//@ts-ignore
import packageConfig from "../../package.json"
import defaultConfig from '../../cep.config';
import { ICepConfig } from "./types";

let g_config: any = ''
interface CepPluginOptions {
    cepConfig?: ICepConfig;
    jsxInput?: string;
    jsxOutput?: string;
    jsxIncludes?: string[];
}

export default function cepPlugin(options: CepPluginOptions = {}) {
    const config = options.cepConfig || defaultConfig;
    return {
        name: 'transform-file',
        async buildStart(viteConfig: any) {
            // 已移除 JSX 构建逻辑，现在使用内联 JSX 方式
            if (process.env.NODE_ENV === 'production') {
                console.log('正式环境 - 使用内联 JSX');
            }
        },
        transform(src: any, id: any) {

        },
        configResolved(viteConfig: any) {
            g_config = viteConfig
            if (viteConfig.isProduction)
                return console.log('[cepPlugin]打包不处理');
            // 已移除 JSX 监听构建，现在使用内联 JSX 方式
            console.log('[cepPlugin] 使用内联 JSX，无需构建外部文件');
            
            const name = `${getProjectName(viteConfig.root)}-dev`
            // 使用配置的端口（strictPort: true 确保端口不会变）
            const port = viteConfig.server?.port || 5180
            const serverURL = `http://localhost:${port}/`
            
            try {
                const cepConfig = createConfig(viteConfig.root, {
                    name: name,
                    id: `com.${name}`,
                    version: packageConfig.version,
                }, "dev")
                copyCepToDev({
                    serverURL: serverURL,
                    name: name,
                    isBuild: false
                }, cepConfig)
            } catch (error) {
                console.log('[CEP] 初始化失败');
                console.log(error);
            }
        },
        async closeBundle() {
            if (!g_config.isProduction)
                return console.log('[cepPlugin]开发环境不处理');

            // await buildJsxByProd()
            const name = `${getProjectName(g_config.root)}`
            try {
                // Use the provided config instead of recreating from package.json if possible, 
                // but createConfig merges simple props. 
                // Wait, createConfig uses hardcoded template logic. 
                // Let's passed detailed config if needed.
                // For now, we trust config passed in options.
                
                // Note: createConfig logic might need review if we want full Custom Config control.
                // But typically it uses the 'config' object we imported/selected at top.
                
                // Actually createConfig generates the manifest content string.
                // We should pass our 'config' object to the copy/write logic.
                
                console.log('[id]:' + config.id);

                copyCepToProd({
                    // 方案 B：CEP 插件打开后直接跳转到服务器 Shell 登录页
                    serverURL: 'https://aidg168.uk/shell/#/login',
                    name: name,
                    isBuild: true,
                    distDir: g_config.build.outDir
                }, config)
            } catch (error) {
                console.log('[CEP] 初始化失败');
                console.log(error);
            }
            console.log('[cepPlugins] 编译成功');
        }
    }
}

function getProjectName(root: string) {
    if(root.endsWith("src/launcher")) return "Designer"; // Hack for launcher root? No, Vite root usually project root.
    return root.split('/').pop()
}