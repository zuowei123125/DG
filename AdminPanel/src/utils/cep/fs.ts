import { isNodeJSEnabled } from "./tool"

/**
 * cep_node 为ps内置的全局变量
 */
//@ts-ignore
export const fs = (isNodeJSEnabled() ? cep_node.require('fs') : {}) as typeof import('fs')