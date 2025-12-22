import { ICepConfig } from "./plugins";

const config: ICepConfig = {
    "name": "AdminPanel",
    "id": "com.designer.adminpanel",
    "version": "1.0.0",
    "extensionVersion": "6.1.0",
    "requiredRuntimeVersion": "8.0",
    "type": "Panel",
    "parameters": [
        "--enable-nodejs"
    ],
    "panels": [
        {
            "name": "AdminPanel",
            "displayName": "ps套版",
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
            "name": "PHSP",
            "version": "[18.0,99.9]"
        },
        {
            "name": "PHXS",
            "version": "[18.0,99.9]"
        }
    ],
    "build": {
        "jsxBin": false,
        "country": "CN",
        "province": "GD",
        "org": "Designer",
        "password": "",
        "tsa": ""
    },
    "zxp": {
        "jsxBin": false
    }
}

export default config;

