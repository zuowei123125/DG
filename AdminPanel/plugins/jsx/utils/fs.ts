import fs from 'fs'
import path from 'path'
import os from 'os'

export const copyFolderSync = (from, to) => {
    if (!fs.existsSync(to)) {
        fs.mkdirSync(to);
    }

    fs.readdirSync(from).forEach((element) => {
        const srcPath = path.join(from, element);
        const destPath = path.join(to, element);

        if (fs.lstatSync(srcPath).isFile()) {
            fs.copyFileSync(srcPath, destPath);
        } else {
            copyFolderSync(srcPath, destPath);
        }
    });
};


export function isMac() {
    return os.platform() === 'darwin'
}
