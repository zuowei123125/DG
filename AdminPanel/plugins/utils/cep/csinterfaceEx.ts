import CSInterface, { CSEvent } from "./csinterface";
/**
 * 扩展PS的CSInterface类
 */
export class CSInterfaceEx {
    constructor() {

    }

    /**持久化运行 */
    public persistent() {
        var cs = new CSInterface();
        var event1 = new CSEvent();
        event1.type = "com.adobe.PhotoshopPersistent";
        event1.scope = "APPLICATION";
        event1.extensionId = cs.getExtensionID();
        cs.dispatchEvent(event1);
    }

    /**取消持久化运行 */
    public unPersisten() {
        var cs = new CSInterface();
        var event1 = new CSEvent();
        event1.type = "com.adobe.PhotoshopUnPersistent";
        event1.scope = "APPLICATION";
        event1.extensionId = cs.getExtensionID();
        cs.dispatchEvent(event1);
    }
}

