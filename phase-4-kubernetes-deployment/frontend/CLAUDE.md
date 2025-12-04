# Frontend: Next.js 16 Application

## Overview

Next.js 16 frontend with Better Auth for authentication, Drizzle ORM for database access, and Tailwind CSS for styling.

## Key Files

- `src/app/layout.tsx` - Root layout with providers
- `src/app/proxy.ts` - Auth protection (replaces middleware)
- `src/app/api/auth/[...all]/route.ts` - Better Auth handler
- `src/lib/auth.ts` - Better Auth server config
- `src/lib/auth-client.ts` - Better Auth client
- `src/lib/api.ts` - FastAPI client with JWT
- `src/lib/db.ts` - Drizzle database client

## Next.js 16 Patterns

### Async Params (IMPORTANT)
Dynamic route params are now Promises in Next.js 15+:

```typescript
// CORRECT - Next.js 15/16
export default async function Page({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params;
  // use id
}

// WRONG - Old pattern
export default function Page({ params }: { params: { id: string } }) {
  // This will NOT work in Next.js 15+
}
```

### Auth Protection with proxy.ts
```typescript
// src/app/proxy.ts
import { createAuthProxy } from 'better-auth/next-js';
import { auth } from '@/lib/auth';

export const { GET, POST } = createAuthProxy(auth);
```

### Server vs Client Components
- Server Components: Data fetching, no useState/useEffect
- Client Components: Add "use client" for interactivity

## Commands

```bash
pnpm dev          # Start dev server
pnpm build        # Build for production
pnpm start        # Start production server
pnpm lint         # Run ESLint
```

## Dependencies

- next: 16.x
- better-auth: Authentication
- drizzle-orm: Database ORM
- @neondatabase/serverless: Neon driver
- tailwindcss: Styling
