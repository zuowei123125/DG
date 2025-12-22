import CSInterface, { SystemPath } from "./csinterface"

export class CEPPath {
    constructor() {

    }

    static getUserData(): string {
        const cs = new CSInterface()
        return cs.getSystemPath(SystemPath.USER_DATA)
    }
    static getCommonFiles() {
        const cs = new CSInterface()
        return cs.getSystemPath(SystemPath.COMMON_FILES)
    }

    static getMyDocuments(): string {
        const cs = new CSInterface()
        return cs.getSystemPath(SystemPath.MY_DOCUMENTS)
    }

    static getApplication(): string {
        const cs = new CSInterface()
        return cs.getSystemPath(SystemPath.APPLICATION)
    }

    static getExtension(): string {
        const cs = new CSInterface()
        return cs.getSystemPath(SystemPath.EXTENSION)
    }

    static getHostApplication(): string {
        const cs = new CSInterface()
        return cs.getSystemPath(SystemPath.HOST_APPLICATION)
    }
}