import { isNodeJSEnabled } from "./tool"
console.error('isNodeJSEnabled()'+isNodeJSEnabled());

/**
 * cep_node 为ps内置的全局变量
 */
//@ts-ignore
export const path = (isNodeJSEnabled() ? cep_node.require('path') : {}) as typeof import('path')

