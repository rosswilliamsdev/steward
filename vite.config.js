import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, 'static/js'),
    emptyOutDir: false, // Don't delete other static files
    rollupOptions: {
      input: path.resolve(__dirname, 'frontend/src/main.jsx'),
      output: {
        entryFileNames: 'donor-dashboard.js',
        assetFileNames: 'donor-dashboard.[ext]'
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'frontend/src')
    }
  }
})
