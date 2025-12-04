import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

const BACKEND_URL = process.env.BACKEND_URL || "http://todo-app-backend:8000";

export async function POST(request: NextRequest) {
  try {
    // Get the session from Better Auth
    const session = await auth.api.getSession({
      headers: await headers(),
    });

    console.log("ChatKit proxy - Session:", session?.session?.id);

    if (!session?.session) {
      console.log("ChatKit proxy - No session found");
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Get JWT token for the backend
    const tokenResponse = await auth.api.getToken({
      headers: await headers(),
    });

    console.log("ChatKit proxy - Token response type:", typeof tokenResponse);
    console.log("ChatKit proxy - Token response:", JSON.stringify(tokenResponse).substring(0, 100));

    // Extract the token - it might be a string or an object with a token property
    const token = typeof tokenResponse === 'string'
      ? tokenResponse
      : (tokenResponse as { token?: string })?.token;

    if (!token) {
      console.log("ChatKit proxy - No token extracted from response");
      return NextResponse.json({ error: "No token available" }, { status: 401 });
    }

    console.log("ChatKit proxy - Token extracted, length:", token.length);

    // Get the request body
    const body = await request.text();

    // Forward the request to the backend
    const backendResponse = await fetch(`${BACKEND_URL}/api/chatkit`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: body,
    });

    console.log("ChatKit proxy - Backend response status:", backendResponse.status);

    // Check if it's a streaming response
    const contentType = backendResponse.headers.get("content-type");

    if (contentType?.includes("text/event-stream")) {
      // Return streaming response
      return new Response(backendResponse.body, {
        headers: {
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          Connection: "keep-alive",
        },
      });
    }

    // Return JSON response
    const data = await backendResponse.json();
    return NextResponse.json(data, { status: backendResponse.status });
  } catch (error) {
    console.error("ChatKit proxy error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
