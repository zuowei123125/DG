import { defineConfig } from 'vite'
import tsconfigPaths from 'vite-tsconfig-paths'
import vue from '@vitejs/plugin-vue'
import cepPlugin from './plugins/jsx/cepPlugin'
import legacy from '@vitejs/plugin-legacy'
import path from 'path'

const isDev = process.env.NODE_ENV !== 'production'

export default defineConfig(({ command }) => {
  const isBuild = command === 'build';
  return {
    server: {
      port: 5180,  // AdminPanel 专用端口
      strictPort: true,  // 强制使用此端口，如果被占用则报错
      cors: true
    },
    plugins: [
      legacy({
        targets: ['chrome 41', 'not IE 11']
      }),
      !isBuild && cepPlugin(),  // 开发时自动复制到 PS 扩展目录
      vue(),
      tsconfigPaths(),
    ],
    base: './',
    resolve: {
      alias: {
        "@/": new URL("./src/", import.meta.url).pathname,
        '@plugins': path.resolve(__dirname, './plugins')
      }
    },
    define: {
      __BUILD_TIME__: Date.now(),
      __DEV__: isDev,
      __VERSION__: JSON.stringify(process.env.npm_package_version),
    },
    build: {
      outDir: 'dist',
      rollupOptions: {
        input: path.resolve(__dirname, 'index.html')
      }
    }
  }
})

