import { ICepConfig } from "@plugins";

const config: ICepConfig = {
    name: "cepName",
    id: "com.cepName",
    version: "1.0.0",
    extensionVersion: "6.1.0",
    requiredRuntimeVersion: "9.0",
    type: "Panel",
    parameters: [
        "--enable-nodejs",
    ],
    panels: [
        {
            name: "cepName",
            displayName: "panelName",
            main: "./index.html",
            width: 400,
            height: 300,
            minWidth: 400,
            minHeight: 300,
            maxWidth: 4000,
            maxHeight: 3000,
        }
    ],
    hosts:[
        {
            name: "AEFT",
            version: "[0.0,99.9]",
          },
          {
            name: "PPRO",
            version: "[0.0,99.9]",
          },
          {
            name: "ILST",
            version: "[0.0,99.9]",
          },
          {
            name: "PHXS",
            version: "[0.0,99.9]",
          },
          {
            name: "FLPR",
            version: "[0.0,99.9]",
          },
    ],
    build: {
        jsxBin: false,
        /**国家 */
        country: "CN",
        /**省份 */
        province: "GD",
        /**公司名称 */
        org: "你的公司名称",
        /**签名密码 */
        password: "",
        tsa: "",
    },
    zxp: {
        jsxBin: false
    }
}

export default config;  