import { ICepConfig } from "./plugins";

const config: ICepConfig = {
    "name": "cep-super-edition",
    "id": "com.cep-super-edition",
    "version": "0.0.1",
    "extensionVersion": "6.1.0",
    "requiredRuntimeVersion": "8.0",
    "type": "Panel",
    "parameters": [
        "--enable-nodejs"
    ],
    "panels": [
        {
            "name": "超级套版",
            "displayName": "超级套版",
            "main": "./index.html",
            "width": 280,
            "height": 600,
            "minWidth": 280,
            "minHeight": 600,
            "maxWidth": 600,
            "maxHeight": 4080
        }
    ],
    "hosts": [
        {
            "name": "AEFT",
            "version": "[0.0,99.9]"
        },
        {
            "name": "PPRO",
            "version": "[0.0,99.9]"
        },
        {
            "name": "ILST",
            "version": "[0.0,99.9]"
        },
        {
            "name": "PHXS",
            "version": "[0.0,99.9]"
        },
        {
            "name": "FLPR",
            "version": "[0.0,99.9]"
        }
    ],
    "build": {
        "jsxBin": false,
        "country": "CN",
        "province": "GD",
        "org": "你的公司名称",
        "password": "",
        "tsa": ""
    },
    "zxp": {
        "jsxBin": false
    }
}

export default config;  