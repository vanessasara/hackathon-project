import { NextResponse } from 'next/server';

/**
 * Health Check Endpoint for Kubernetes Probes
 * Used by readinessProbe and livenessProbe
 *
 * Returns 200 OK if the application is healthy
 */
export async function GET() {
  try {
    // Basic health check - application is running
    const healthStatus = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'frontend',
      version: process.env.npm_package_version || '3.0.0',
    };

    return NextResponse.json(healthStatus, { status: 200 });
  } catch (error) {
    // If something goes wrong, return 503 Service Unavailable
    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        service: 'frontend',
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 503 }
    );
  }
}
