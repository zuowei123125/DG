/// <reference types="types-for-adobe/Photoshop/2015.5"/>

// CSInterface/CEP 的最小化类型定义，避免 TS 编译报错
declare class CSInterface {
    constructor();
    getHostEnvironment(): any;
    addEventListener(type: string, listener: any, obj?: any): void;
    evalScript(script: string, callback?: (result: string) => void): void;
    openURLInDefaultBrowser(url: string): void;
    closeExtension(): void;
}

declare interface HostEnvironment {
    appSkinInfo: any;
}

declare interface CSEvent {
    type: string;
    data: any;
}

/**
 * cep.ts
 * Adobe CSInterface 的封装类，提供类型安全和环境判断
 */

class CepWrapper {
    private csInterface: CSInterface | null = null;
    public inCEP: boolean = false;

    constructor() {
        // @ts-ignore
        if (typeof CSInterface !== 'undefined') {
            // @ts-ignore
            this.csInterface = new CSInterface();
            this.inCEP = true;
        } else {
            // 延迟导入 logger 以避免循环依赖
            import('./logger').then(({ logger }) => {
                logger.warn('未找到 CSInterface，当前运行于浏览器模式。');
            });
        }
    }

    /**
     * 获取原始 CSInterface 实例
     */
    public getCSInterface(): CSInterface | null {
        return this.csInterface;
    }

    /**
     * 获取宿主环境信息 (如皮肤颜色、版本等)
     */
    public getHostEnvironment(): HostEnvironment | null {
        if (this.csInterface) {
            return this.csInterface.getHostEnvironment();
        }
        return null;
    }

    /**
     * 添加 CEP 事件监听
     */
    public addEventListener(type: string, listener: (event: CSEvent) => void, obj?: any): void {
        if (this.csInterface) {
            this.csInterface.addEventListener(type, listener, obj);
        }
    }

    /**
     * 执行 ExtendScript (JSX) 脚本
     * 返回 Promise 封装的结果
     */
    public evalScript(script: string): Promise<string> {
        return new Promise((resolve, reject) => {
            if (!this.csInterface) {
                // 浏览器模式下的模拟行为
                import('./logger').then(({ logger }) => {
                    logger.log(`[Mock CEP] 执行脚本: ${script}`);
                });
                // 返回合法的 JSON 字符串以避免 Parse Error
                resolve('{"success": true, "message": "MOCK_RESULT"}'); 
                return;
            }
            
            this.csInterface.evalScript(script, (result: string) => {
                if (result === 'EvalScript error.') {
                    reject(new Error(result));
                } else {
                    resolve(result);
                }
            });
        });
    }

    /**
     * 在默认系统浏览器中打开 URL
     */
    public openURLInDefaultBrowser(url: string): void {
        if (this.csInterface) {
            this.csInterface.openURLInDefaultBrowser(url);
        } else {
            window.open(url, '_blank');
        }
    }
    
    /**
     * 关闭扩展面板
     */
    public closeExtension(): void {
        this.csInterface?.closeExtension();
    }
}

export const cep = new CepWrapper();
