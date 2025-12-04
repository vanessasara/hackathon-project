"""
JWT verification for Better Auth tokens.

This module provides JWT verification using the JWKS endpoint from Better Auth
and extracts the user ID from the token's 'sub' claim.
"""

import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import lru_cache
from .config import settings

security = HTTPBearer()


@lru_cache(maxsize=1)
def get_jwk_client() -> PyJWKClient:
    """
    Get a cached PyJWKClient for JWKS verification.

    The client fetches public keys from Better Auth's JWKS endpoint
    and caches them for efficient verification.

    Returns:
        PyJWKClient: Configured JWKS client
    """
    jwks_url = f"{settings.better_auth_url}/api/auth/jwks"
    return PyJWKClient(jwks_url)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Verify JWT token and extract user ID.

    This dependency extracts the JWT from the Authorization header,
    verifies its signature using JWKS, and returns the user ID from
    the 'sub' claim.

    Args:
        credentials: HTTP Bearer token credentials

    Returns:
        str: User ID from token's 'sub' claim

    Raises:
        HTTPException: 401 if token is invalid or missing user ID
    """
    token = credentials.credentials

    try:
        # Get JWKS client and signing key
        jwk_client = get_jwk_client()
        signing_key = jwk_client.get_signing_key_from_jwt(token)

        # Verify and decode the JWT
        # Better Auth uses EdDSA (Ed25519) by default
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["EdDSA", "RS256"],
            options={"verify_aud": False}  # Better Auth doesn't use audience claim
        )

        # Extract user ID from 'sub' claim
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )

        return user_id

    except jwt.exceptions.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )


async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Verify JWT token and extract user information.

    This dependency extracts the JWT from the Authorization header,
    verifies its signature using JWKS, and returns user info including
    id, name, and email from the JWT payload.

    Args:
        credentials: HTTP Bearer token credentials

    Returns:
        dict: User information with id, name, and email

    Raises:
        HTTPException: 401 if token is invalid or missing user ID
    """
    token = credentials.credentials

    try:
        # Get JWKS client and signing key
        jwk_client = get_jwk_client()
        signing_key = jwk_client.get_signing_key_from_jwt(token)

        # Verify and decode the JWT
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["EdDSA", "RS256"],
            options={"verify_aud": False}
        )

        # Extract user information from claims
        user_id = payload.get("sub")
        name = payload.get("name")
        email = payload.get("email")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )

        return {
            "id": user_id,
            "name": name,
            "email": email,
        }

    except jwt.exceptions.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
