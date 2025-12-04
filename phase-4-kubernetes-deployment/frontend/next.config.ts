import type { NextConfig } from "next";

// Backend URL - use Kubernetes service name for container deployment
// In local dev, use localhost:8000
const BACKEND_URL = process.env.BACKEND_URL ||
  (process.env.NODE_ENV === 'production'
    ? 'http://todo-app-backend:8000'
    : 'http://localhost:8000');

const nextConfig: NextConfig = {
  output: 'standalone', // For Docker deployment
  async rewrites() {
    return [
      {
        // Proxy task API endpoints to backend
        source: '/api/tasks/:path*',
        destination: `${BACKEND_URL}/api/tasks/:path*`,
      },
      {
        // Proxy label API endpoints to backend
        source: '/api/labels/:path*',
        destination: `${BACKEND_URL}/api/labels/:path*`,
      },
      {
        // Proxy image API endpoints to backend
        source: '/api/images/:path*',
        destination: `${BACKEND_URL}/api/images/:path*`,
      },
      {
        // Proxy chat API endpoints to backend
        source: '/api/chat/:path*',
        destination: `${BACKEND_URL}/api/chat/:path*`,
      },
      // ChatKit endpoint handled by /api/chatkit/route.ts (needs auth header injection)
    ];
  },
};

export default nextConfig;
