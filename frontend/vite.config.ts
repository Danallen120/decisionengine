/// <reference types="vitest/config" />
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// The built UI is served by the local API (`decision-engine serve`), same origin, no CORS.
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "../src/decision_engine/api/static",
    emptyOutDir: true,
    sourcemap: false,
  },
  server: {
    host: "127.0.0.1",
    proxy: { "/v1": "http://127.0.0.1:8000" },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test-setup.ts"],
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],
      exclude: ["src/main.tsx", "src/test-setup.ts", "src/**/*.test.{ts,tsx}"],
      thresholds: { lines: 80, branches: 80, functions: 80, statements: 80 },
    },
  },
});
