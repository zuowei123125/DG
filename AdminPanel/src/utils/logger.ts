/**
 * 全局日志管理工具
 * 
 * 提供统一的日志管理，支持一键开启/关闭所有日志
 * 
 * @example
 * import { logger } from '@/utils/logger';
 * 
 * // 使用日志
 * logger.log('普通日志');
 * logger.info('信息日志');
 * logger.warn('警告日志');
 * logger.error('错误日志');
 * logger.debug('调试日志');
 * 
 * // 控制日志开关
 * logger.enable();   // 开启日志
 * logger.disable();  // 关闭日志
 * 
 * // 或者设置
 * logger.setEnabled(true);  // 开启
 * logger.setEnabled(false); // 关闭
 */

type LogLevel = 'log' | 'info' | 'warn' | 'error' | 'debug';

class Logger {
    private _enabled: boolean = false;  // 默认关闭日志
    
    /**
     * 获取日志开启状态
     */
    get enabled(): boolean {
        return this._enabled;
    }
    
    /**
     * 开启日志
     */
    enable(): void {
        this._enabled = true;
        console.log('[Logger] 日志已开启');
    }
    
    /**
     * 关闭日志
     */
    disable(): void {
        console.log('[Logger] 日志已关闭');
        this._enabled = false;
    }
    
    /**
     * 设置日志开启状态
     */
    setEnabled(enabled: boolean): void {
        if (enabled) {
            this.enable();
        } else {
            this.disable();
        }
    }
    
    /**
     * 切换日志状态
     */
    toggle(): void {
        this.setEnabled(!this._enabled);
    }
    
    /**
     * 普通日志
     */
    log(...args: any[]): void {
        if (this._enabled) {
            console.log(...args);
        }
    }
    
    /**
     * 信息日志
     */
    info(...args: any[]): void {
        if (this._enabled) {
            console.info(...args);
        }
    }
    
    /**
     * 警告日志
     */
    warn(...args: any[]): void {
        if (this._enabled) {
            console.warn(...args);
        }
    }
    
    /**
     * 错误日志 - 错误日志始终显示，不受开关控制
     * 如果需要控制错误日志，使用 errorSilent
     */
    error(...args: any[]): void {
        // 错误日志始终输出，便于调试问题
        console.error(...args);
    }
    
    /**
     * 可控制的错误日志
     */
    errorSilent(...args: any[]): void {
        if (this._enabled) {
            console.error(...args);
        }
    }
    
    /**
     * 调试日志
     */
    debug(...args: any[]): void {
        if (this._enabled) {
            console.debug(...args);
        }
    }
    
    /**
     * 分组日志开始
     */
    group(...args: any[]): void {
        if (this._enabled) {
            console.group(...args);
        }
    }
    
    /**
     * 分组日志结束
     */
    groupEnd(): void {
        if (this._enabled) {
            console.groupEnd();
        }
    }
    
    /**
     * 折叠分组日志开始
     */
    groupCollapsed(...args: any[]): void {
        if (this._enabled) {
            console.groupCollapsed(...args);
        }
    }
    
    /**
     * 表格日志
     */
    table(data: any, columns?: string[]): void {
        if (this._enabled) {
            console.table(data, columns);
        }
    }
    
    /**
     * 分隔线日志
     */
    separator(char: string = '=', length: number = 60): void {
        if (this._enabled) {
            console.log(char.repeat(length));
        }
    }
}

// 导出单例
export const logger = new Logger();

// 默认导出
export default logger;

// 在开发环境下，可以通过 window.logger 访问
if (typeof window !== 'undefined') {
    (window as any).logger = logger;
}

