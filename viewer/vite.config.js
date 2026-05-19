import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiUrl = env.VITE_API_URL || 'http://localhost:7860';
  const baseUrl = env.VITE_BASE_URL || '/';

  return {
    base: baseUrl,
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: false,   // disable in prod to reduce bundle size
      rollupOptions: {
        output: {
          manualChunks: {
            three: ['three'],
          }
        }
      }
    },
    server: {
      port: 3000,
      open: true
    },
    define: {
      // Makes __API_URL__ available in all TS/JS source files
      __API_URL__: JSON.stringify(apiUrl),
    }
  };
});
