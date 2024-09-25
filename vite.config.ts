// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: '/rutube-recommendations/', // Замените на имя вашего репозитория
  build: {
    outDir: 'dist',
  },
})