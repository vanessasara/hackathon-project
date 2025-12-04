import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "",  // Empty string uses current origin
  plugins: [jwtClient()],
});

export const { signIn, signUp, signOut, useSession } = authClient;
export const getToken = authClient.token;
