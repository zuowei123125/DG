export type ICepConfig = {
    name: string
    id: string
    version: string
    extensionVersion: string
    requiredRuntimeVersion: string
    type: "Panel"
    parameters: IParameter[]
    panels: IPanel[],
    hosts?: {name:string,version:string}[]
    build: {
        jsxBin: boolean
        /**国家 */
        country: string,
        /**省份 */
        province: string,
        /**公司名称 */
        org: string
        /**签名密码 */
        password: string,
        tsa: string,
    },
    zxp: {
        jsxBin: boolean
    }
}

type IParameter = "--enable-nodejs" | "--enable-media-stream" | "--enable-speech-input"

export type IPanel = {
    /**入口index.html */
    main:string
    name: string
    /**插件名称 */
    displayName:string
    width: number
    height: number
    minWidth?: number
    minHeight?: number
    maxWidth?: number
    maxHeight?: number
}