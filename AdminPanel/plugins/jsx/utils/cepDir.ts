import { isMac } from "./fs"
import os from 'os'
import path from 'path'

function getUserDataPath() {
    if (process.platform === 'darwin') {
        return path.join(os.homedir(), 'Library', 'Application Support');
    } else if (process.platform === 'win32') {
        return path.join(process.env.APPDATA);
    } else {
        return path.join(os.homedir());
    }
}
export function getAdobeCepDir() {
    const mac = path.join(getUserDataPath(), 'Adobe/CEP/extensions')
    const win = path.join(getUserDataPath(), 'Adobe/CEP/extensions')
    return isMac() ? mac : win
}
