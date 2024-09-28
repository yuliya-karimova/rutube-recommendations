import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/dist/',
  // base: '/rutube-recommendations/', // Замените на имя вашего репозитория
  build: {
    outDir: 'dist',
  },
})
