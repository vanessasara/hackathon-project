---
name: nextjs
description: Next.js 16 patterns for App Router, Server/Client Components, proxy.ts authentication, data fetching, caching, and React Server Components. Use when building Next.js applications with modern patterns.
---

# Next.js 16 Skill

Modern Next.js patterns for App Router, Server Components, and the new proxy.ts authentication pattern.

## Quick Start

### Installation

```bash
# npm
npx create-next-app@latest my-app

# pnpm
pnpm create next-app my-app

# yarn
yarn create next-app my-app

# bun
bun create next-app my-app
```

## App Router Structure

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page
├── proxy.ts            # Auth proxy (replaces middleware.ts)
├── (auth)/
│   ├── login/page.tsx
│   └── register/page.tsx
├── (dashboard)/
│   ├── layout.tsx
│   └── page.tsx
├── api/
│   └── [...route]/route.ts
└── globals.css
```

## Key Concepts

| Concept | Guide |
|---------|-------|
| **Server vs Client Components** | [reference/components.md](reference/components.md) |
| **proxy.ts (Auth)** | [reference/proxy.md](reference/proxy.md) |
| **Data Fetching** | [reference/data-fetching.md](reference/data-fetching.md) |
| **Caching** | [reference/caching.md](reference/caching.md) |
| **Route Handlers** | [reference/route-handlers.md](reference/route-handlers.md) |

## Examples

| Pattern | Guide |
|---------|-------|
| **Authentication Flow** | [examples/authentication.md](examples/authentication.md) |
| **Protected Routes** | [examples/protected-routes.md](examples/protected-routes.md) |
| **Forms & Actions** | [examples/forms-actions.md](examples/forms-actions.md) |
| **API Integration** | [examples/api-integration.md](examples/api-integration.md) |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/proxy.ts](templates/proxy.ts) | Auth proxy template |
| [templates/layout.tsx](templates/layout.tsx) | Root layout with providers |
| [templates/page.tsx](templates/page.tsx) | Page component template |

## proxy.ts (Next.js 16)

**IMPORTANT**: Next.js 16 replaces `middleware.ts` with `proxy.ts`. The proxy runs on Node.js runtime (not Edge).

```typescript
// app/proxy.ts
import { NextRequest, NextResponse } from "next/server";

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check auth for protected routes
  const token = request.cookies.get("better-auth.session_token");

  if (pathname.startsWith("/dashboard") && !token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/api/:path*"],
};
```

## Server Components (Default)

```tsx
// app/posts/page.tsx - Server Component by default
async function PostsPage() {
  const posts = await fetch("https://api.example.com/posts", {
    cache: "force-cache", // or "no-store"
  }).then(res => res.json());

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}

export default PostsPage;
```

## Client Components

```tsx
"use client";

import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

## Server Actions

```tsx
// app/actions.ts
"use server";

import { revalidatePath } from "next/cache";

export async function createPost(formData: FormData) {
  const title = formData.get("title") as string;

  await db.post.create({ data: { title } });

  revalidatePath("/posts");
}
```

```tsx
// app/posts/new/page.tsx
import { createPost } from "../actions";

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Post title" />
      <button type="submit">Create</button>
    </form>
  );
}
```

## Data Fetching Patterns

### Parallel Data Fetching

```tsx
async function Page() {
  const [user, posts] = await Promise.all([
    getUser(),
    getPosts(),
  ]);

  return <Dashboard user={user} posts={posts} />;
}
```

### Sequential Data Fetching

```tsx
async function Page() {
  const user = await getUser();
  const posts = await getUserPosts(user.id);

  return <Dashboard user={user} posts={posts} />;
}
```

## Environment Variables

```env
# .env.local
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret
NEXT_PUBLIC_API_URL=http://localhost:8000
```

- `NEXT_PUBLIC_*` - Exposed to browser
- Without prefix - Server-only

## Common Patterns

### Layout with Auth Provider

```tsx
// app/layout.tsx
import { AuthProvider } from "@/components/auth-provider";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
```

### Loading States

```tsx
// app/posts/loading.tsx
export default function Loading() {
  return <div>Loading posts...</div>;
}
```

### Error Handling

```tsx
// app/posts/error.tsx
"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```
