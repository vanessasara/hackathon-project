# Research: Full-Stack Web Todo Application

**Feature**: 002-fullstack-web-app
**Date**: 2025-12-02
**Status**: Complete

## Research Areas

### 1. Authentication Strategy

**Decision**: Better Auth with JWT for cross-service authentication

**Rationale**:
- Better Auth is a modern, framework-agnostic TypeScript auth library
- Built-in JWT support allows stateless verification in FastAPI backend
- Supports email/password out of the box (MVP requirement)
- JWKS endpoint enables secure JWT verification without shared secrets
- Session management handled automatically

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| NextAuth.js | Less flexible for cross-service JWT, primarily session-based |
| Auth0 | Overkill for hackathon, adds external dependency |
| Custom JWT | Reinventing the wheel, security risks |
| Clerk | Paid service, unnecessary for MVP |

### 2. Frontend Framework

**Decision**: Next.js 16 with App Router

**Rationale**:
- Server Components reduce client-side JavaScript
- App Router provides modern routing patterns
- proxy.ts replaces middleware for auth (Node.js runtime)
- Built-in API routes for Better Auth handler
- Excellent TypeScript support
- Easy deployment to Vercel

**Key Patterns**:
- `proxy.ts` for authentication (NOT middleware.ts)
- Async params in dynamic routes (`params: Promise<{id: string}>`)
- Server Components for data fetching
- Client Components for interactivity

### 3. Backend Framework

**Decision**: FastAPI with SQLModel

**Rationale**:
- Continues Python from Phase I (consistency)
- FastAPI provides automatic OpenAPI documentation
- SQLModel combines Pydantic validation with SQLAlchemy ORM
- Async support for better performance
- Excellent dependency injection for auth

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Django REST | Heavier, more opinionated |
| Flask | Less modern, manual validation |
| Express.js | Would require full JavaScript stack |

### 4. Database Choice

**Decision**: Neon Serverless PostgreSQL

**Rationale**:
- Serverless scales automatically
- Free tier sufficient for hackathon
- Database branching for development workflow
- Compatible with both Drizzle ORM (TS) and SQLModel (Python)
- Connection pooling built-in

**Connection Strategy**:
- Frontend (direct reads): Drizzle ORM with HTTP driver
- Backend (all writes): SQLModel with connection pooling

### 5. ORM Strategy

**Decision**: Dual ORM approach - Drizzle (TypeScript) + SQLModel (Python)

**Rationale**:
- Drizzle for Next.js Server Components (direct DB reads)
- SQLModel for FastAPI (business logic, writes)
- Both are type-safe
- Better Auth integrates with Drizzle adapter

**Schema Management**:
- Better Auth CLI generates auth tables
- Drizzle Kit for migrations
- SQLModel models must match Drizzle schema

### 6. Styling Approach

**Decision**: Tailwind CSS

**Rationale**:
- Utility-first CSS for rapid development
- No separate CSS files to manage
- Responsive design built-in
- Works well with Server Components

### 7. JWT Verification (Python)

**Decision**: PyJWT with JWKS fetching via httpx

**Rationale**:
- PyJWT is the standard JWT library for Python
- JWKS endpoint provides public keys for verification
- httpx for async HTTP requests
- Cache JWKS with TTL for performance

**Implementation**:
```python
# Fetch JWKS from Better Auth
GET {BETTER_AUTH_URL}/.well-known/jwks.json

# Verify JWT using public key
jwt.decode(token, public_key, algorithms=["RS256"])
```

## Technology Stack Summary

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend Framework | Next.js | 16+ |
| Frontend Language | TypeScript | 5.x |
| UI Styling | Tailwind CSS | 3.x |
| Auth Library | Better Auth | Latest |
| Frontend ORM | Drizzle ORM | Latest |
| Backend Framework | FastAPI | 0.109+ |
| Backend Language | Python | 3.13+ |
| Backend ORM | SQLModel | Latest |
| Database | Neon PostgreSQL | Serverless |
| JWT Library | PyJWT | 2.8+ |
| HTTP Client | httpx | 0.26+ |

## Unresolved Items

None - all technical decisions made.

## References

- Better Auth Docs: https://better-auth.com
- Next.js 16 Docs: https://nextjs.org/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Drizzle ORM Docs: https://orm.drizzle.team
- Neon Docs: https://neon.tech/docs
