---
id: 0004
title: Implement Better Auth and JWT Verification
stage: implement
date: 2026-01-22
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-fullstack-web-app
branch: 002-fullstack-web-app
user: venisa-sara
command: /sp.implement
labels: ["authentication", "better-auth", "jwt", "fastapi", "nextjs", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - /home/dell/evolution-of-todo/phase-2-web/frontend/src/lib/db.ts
  - /home/dell/evolution-of-todo/phase-2-web/frontend/src/lib/auth.ts
  - /home/dell/evolution-of-todo/phase-2-web/frontend/src/lib/auth-client.ts
  - /home/dell/evolution-of-todo/phase-2-web/frontend/src/app/api/auth/[...all]/route.ts
  - /home/dell/evolution-of-todo/phase-2-web/frontend/src/app/proxy.ts
  - /home/dell/evolution-of-todo/phase-2-web/backend/src/auth.py
  - /home/dell/evolution-of-todo/phase-2-web/backend/tests/test_auth.py
tests:
  - tests/test_auth.py::TestGetJwkClient::test_get_jwk_client_returns_pyjwkclient
  - tests/test_auth.py::TestGetJwkClient::test_get_jwk_client_uses_correct_url
  - tests/test_auth.py::TestGetJwkClient::test_get_jwk_client_is_cached
  - tests/test_auth.py::TestGetCurrentUser::test_valid_token_returns_user_id
  - tests/test_auth.py::TestGetCurrentUser::test_token_without_sub_claim_raises_401
  - tests/test_auth.py::TestGetCurrentUser::test_invalid_jwt_signature_raises_401
  - tests/test_auth.py::TestGetCurrentUser::test_expired_token_raises_401
  - tests/test_auth.py::TestGetCurrentUser::test_malformed_token_raises_401
  - tests/test_auth.py::TestGetCurrentUser::test_jwt_decode_uses_rs256_algorithm
  - tests/test_auth.py::TestGetCurrentUser::test_jwt_decode_disables_audience_verification
---

## Prompt

You are the auth-expert agent. Complete tasks T020-T026 for the Full-Stack Web Todo Application.

## Context
- Working directory: /home/dell/evolution-of-todo/phase-2-web
- Frontend: Next.js 16 in /phase-2-web/frontend/
- Backend: FastAPI in /phase-2-web/backend/
- Database URL: postgresql://zeeshan080:zqm3PNQoZFL8@ep-divine-sun-a5fzzeca-pooler.us-east-2.aws.neon.tech/evolution-of-todo-db?sslmode=require
- BETTER_AUTH_SECRET: evolution-of-todo-super-secret-key-2025
- BETTER_AUTH_URL: http://localhost:3000

## Your Tasks (T020-T026)

### Frontend (Better Auth)
- T020: Configure Better Auth server in frontend/src/lib/auth.ts
- T021: Create Better Auth client in frontend/src/lib/auth-client.ts
- T022: Create Better Auth API route handler in frontend/src/app/api/auth/[...all]/route.ts
- T023: Create proxy.ts for auth protection in frontend/src/app/proxy.ts (Next.js 16 pattern - NOT middleware.ts)

### Backend (JWT Verification)
- T024: Implement JWT verification in backend/src/auth.py
- T025: Create get_current_user dependency in backend/src/auth.py (same file as T024)
- T026: Write pytest tests for JWT verification in backend/tests/test_auth.py

## Response snapshot

Successfully implemented Better Auth authentication for the frontend and JWT verification for the backend.

### Frontend Implementation (Next.js 16)

**1. Database Client (/phase-2-web/frontend/src/lib/db.ts)**
- Created Drizzle database client using Neon serverless driver
- Configured with DATABASE_URL environment variable

**2. Better Auth Server (/phase-2-web/frontend/src/lib/auth.ts)**
- Configured Better Auth with Drizzle adapter for PostgreSQL
- Enabled email/password authentication
- Set up session cookie cache with 5-minute max age

**3. Better Auth Client (/phase-2-web/frontend/src/lib/auth-client.ts)**
- Created React client for authentication
- Exports signIn, signUp, signOut, and useSession hooks
- Configured with NEXT_PUBLIC_BETTER_AUTH_URL

**4. API Route Handler (/phase-2-web/frontend/src/app/api/auth/[...all]/route.ts)**
- Created Next.js 16 API route handler for Better Auth
- Exports GET and POST handlers using toNextJsHandler

**5. Proxy Protection (/phase-2-web/frontend/src/app/proxy.ts)**
- Implemented Next.js 16 auth protection pattern (not middleware.ts)
- Created getSession() function using headers() from next/headers
- Allows server components to check authentication status

### Backend Implementation (FastAPI)

**1. JWT Verification Module (/phase-2-web/backend/src/auth.py)**
- Implemented get_jwk_client() with LRU cache for efficient JWKS fetching
- Created get_current_user() FastAPI dependency
- Fetches public keys from Better Auth's JWKS endpoint
- Verifies JWT signatures using RS256 algorithm
- Extracts user_id from JWT 'sub' claim
- Raises HTTPException 401 for invalid tokens

**2. Comprehensive Test Suite (/phase-2-web/backend/tests/test_auth.py)**
- 10 tests covering all authentication scenarios
- Tests JWKS client initialization and caching
- Tests valid token verification and user ID extraction
- Tests error cases: missing sub claim, invalid signature, expired token, malformed token
- Tests correct algorithm (RS256) and options (verify_aud: false)
- All 10 tests passed successfully

## Outcome

- ✅ Impact: Complete authentication infrastructure for Phase 2 full-stack web application. Frontend can authenticate users via Better Auth, backend can verify JWT tokens.
- 🧪 Tests: 10/10 pytest tests passing in backend/tests/test_auth.py
- 📁 Files: 7 files created (4 frontend, 2 backend, 1 test)
- 🔁 Next prompts: Implement database schema with Drizzle, create Task CRUD endpoints, build UI components
- 🧠 Reflection: Implementation follows Next.js 16 patterns (proxy.ts instead of middleware.ts) and Better Auth best practices. JWT verification uses JWKS for secure token validation without sharing secrets.

## Evaluation notes (flywheel)

- Failure modes observed: None - all tests passed on first run
- Graders run and results (PASS/FAIL): PASS - 10/10 tests passing
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test authentication flow end-to-end with actual Better Auth server running
