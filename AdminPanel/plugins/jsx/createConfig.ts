
import fs from 'fs';
import path from 'path';
import defConfig from './template/cep.config';
import { ICepConfig } from './types';
const fileName = 'cep.config.ts';

/**
 * 
 * @param root 创建cep.config.ts
 */
export function createConfig(root: string, config: Partial<ICepConfig>, env: 'dev' | 'prod') {
    // 指定要检查的文件路径
    const filePath = path.resolve(root, env + "." + fileName);

    const temp: ICepConfig = Object.assign({}, defConfig, {
        name: config.name,
        id: config.id,
        version: config.version,
    });

    // 判断文件是否存在
    if (!fs.existsSync(filePath)) {
        // 如果文件不存在，则创建文件
        fs.writeFileSync(filePath, `import { ICepConfig } from "@/plugins";\n\nconst config: ICepConfig = ${JSON.stringify(temp, null, 4)}\n\nexport default config;  `);
        console.log(`[CEP] 添加配置文件 ${fileName} 成功！`);
    } else {
        console.log(`[CEP] 已有配置`);
        return getFileConfig(filePath);
    }
    return temp;
}

function getFileConfig(configPath: string) {
    let temp = fs.readFileSync(configPath, 'utf-8').split('ICepConfig = ')[1];
    const temp2 = temp.split('}')
    temp2.pop()
    const str = temp2.join('}') + '}';
    return JSON.parse(str);
}