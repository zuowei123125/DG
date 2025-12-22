/**是否开启了node模块 */
export function isNodeJSEnabled() {
    //@ts-ignore	
    if (typeof (cep_node) !== 'undefined') {
        //if require and process is available, it should be mixed context
         //@ts-ignore	
        if ((typeof (cep_node.require) !== 'undefined') && (typeof (cep_node.process) !== 'undefined')) {
            return true
        }
        else {
            return false
        }
    }
    else {
        return false
    }
}
