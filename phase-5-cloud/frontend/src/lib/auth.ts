import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { jwt } from "better-auth/plugins";
import { db } from "./db";
import * as schema from "../../drizzle/schema";

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: "pg", schema }),
  emailAndPassword: { enabled: true },
  session: {
    cookieCache: { enabled: true, maxAge: 60 * 5 },
  },
  plugins: [
    jwt({
      jwt: {
        definePayload: ({ user }) => {
          return {
            sub: user.id,
            name: user.name,
            email: user.email,
          };
        },
      },
    }),
  ],
});
