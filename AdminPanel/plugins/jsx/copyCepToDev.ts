import fs from 'fs'
import path from 'path'
import { ICepConfig, IPanel } from './types';
import { joinDebug } from './template/debug';
import { copyFolderSync } from './utils/fs';
import { getAdobeCepDir } from './utils/cepDir';
import { joinManifest } from './template/manifest';
import { joinHtml } from './template/html';
import open from 'open';
/**
 * 复制插件壳到ps插件目录
 */
export function copyCepToDev(options: Omit<IOptions, 'outCepPath' | 'inputCepTemp'>, cepConfig: ICepConfig) {
  cepConfig.panels[0].displayName = `[dev]${cepConfig.panels[0].displayName}`
  const cep = new CEP(options, cepConfig)
  cep.write()
  console.log(`[CEP] 插件壳已就绪`);
  console.log(`[CEP] PS调试地址: http://localhost:7090`);
  open('http://localhost:7090')
}

export function copyCepToProd(options: Omit<IOptions, 'outCepPath' | 'inputCepTemp'>, cepConfig: ICepConfig) {
  cepConfig.panels[0].displayName = `${cepConfig.panels[0].displayName}`
  const cep = new CEP(options, cepConfig)
  cep.write()
}

type IOptions = {
  name: string
  serverURL: string
  outCepPath: string
  inputCepTemp: string
  isBuild: boolean
  distDir?: string // Added dynamic dist path
}

export class CEP {
  constructor(private readonly options: Omit<IOptions, 'outCepPath' | 'inputCepTemp'>, private readonly cepConfig: ICepConfig) {
    this.createDist()
  }

  private get cepInput() {
    return path.join(__dirname, "./template/cep")
  }

  private get dist() {
    if (this.options.distDir) {
        if (path.isAbsolute(this.options.distDir)) return this.options.distDir;
        return path.resolve(process.cwd(), this.options.distDir);
    }
    return path.join(__dirname, '../../dist')
  }

  private get cepOutput() {
    return path.join(this.dist, this.options.name)
  }

  private get cepLink() {
    return path.join(getAdobeCepDir(), this.options.name)
  }

  private get debug() {
    return path.join(this.cepOutput, '.debug')
  }

  private createDist() {
    if (!fs.existsSync(this.dist)) {
      fs.mkdirSync(this.dist)
    }
  }

  public write() {
    this.copyFolder()
    if (!this.options.isBuild)
      this.writeHtml()
    this.writeCSXS()
    if (!this.options.isBuild)
      this.writeDebug()
    this.copyJson2()
    
    // 创建符号链接或直接复制
    if (!fs.existsSync(this.cepLink)) {
      try {
        fs.symlinkSync(this.cepOutput, this.cepLink, 'dir')
        console.log('[CEP] 符号链接已创建')
      } catch (error: any) {
        // 权限不足时，改用复制
        if (error.code === 'EPERM') {
          console.warn('[CEP] 符号链接权限不足，改用复制方式')
          this.copyToCepDir()
        } else {
          throw error
        }
      }
    } else {
      // 目录已存在，需要更新文件
      this.copyToCepDir()
    }

    if (this.options.isBuild) {
      this.copyBuildFiles()
    }

    console.log('[cepPlugin] 安装目录：', getAdobeCepDir());

  }
  
  private copyToCepDir() {
    // 删除旧目录
    if (fs.existsSync(this.cepLink)) {
      fs.rmSync(this.cepLink, { recursive: true, force: true })
    }
    // 复制目录
    copyFolderSync(this.cepOutput, this.cepLink)
    console.log('[CEP] 已复制到 CEP 目录')
  }

  private copyFolder() {
    copyFolderSync(this.cepInput, this.cepOutput)
  }

  private writeHtml() {
    const outhtml = path.join(this.cepOutput, 'index.html')
    let content = joinHtml(this.cepConfig.name, this.options.serverURL || 'http://localhost:5173/')
    fs.writeFileSync(outhtml, content)
  }

  private writeCSXS() {
    const info = joinManifest(this.cepConfig)
    const output = path.join(this.cepOutput, 'CSXS/manifest.xml')
    fs.writeFileSync(output, info)
  }

  private writeDebug() {
    const info = joinDebug(this.cepConfig.id, this.cepConfig.hosts)
    fs.writeFileSync(this.debug, info)
  }

  private copyJson2() {
    const input = path.join(__dirname, '../utils/json')
    const out = path.join(this.cepOutput, 'js')
    copyFolderSync(input, out)
  }

  private copyBuildFiles() {
    // 1. 复制 assets 目录
    const assetsInput = path.join(this.dist, 'assets')
    const assetsOut = path.join(this.cepOutput, 'assets')
    if (fs.existsSync(assetsInput)) {
      copyFolderSync(assetsInput, assetsOut)
      console.log('[CEP] ✓ 已复制 assets 目录')
    }

    // 2. 复制 CSInterface.js
    const csInterfaceSrc = path.join(this.dist, 'CSInterface.js')
    const csInterfaceDst = path.join(this.cepOutput, 'CSInterface.js')
    if (fs.existsSync(csInterfaceSrc)) {
      fs.copyFileSync(csInterfaceSrc, csInterfaceDst)
      console.log('[CEP] ✓ 已复制 CSInterface.js')
    }

    // 3. 复制并修正 HTML 路径
    const builtHtmlPath = path.join(this.dist, 'src/launcher/index.html')
    const targetHtmlPath = path.join(this.cepOutput, 'index.html')
    
    if (fs.existsSync(builtHtmlPath)) {
      // 读取 HTML 内容并修正路径
      let htmlContent = fs.readFileSync(builtHtmlPath, 'utf-8')
      
      // 修正路径：把 ../../ 替换成 ./
      htmlContent = htmlContent.replace(/\.\.\/\.\.\//g, './')
      // 确保 CSInterface.js 路径正确
      htmlContent = htmlContent.replace(/src="\.\/CSInterface\.js"/g, 'src="CSInterface.js"')
      
      fs.writeFileSync(targetHtmlPath, htmlContent)
      console.log('[CEP] ✓ 已复制并修正 HTML 路径')
    } else {
      console.warn('[CEP] ✗ 未找到构建的 HTML:', builtHtmlPath)
    }
  }
}
