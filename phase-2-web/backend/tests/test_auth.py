"""
Tests for JWT authentication and verification.

These tests verify that the auth module correctly verifies JWT tokens
from Better Auth and extracts user IDs.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import PyJWTError

from src.auth import get_current_user, get_jwk_client


class TestGetJwkClient:
    """Tests for JWKS client initialization."""

    def test_get_jwk_client_returns_pyjwkclient(self):
        """Test that get_jwk_client returns a PyJWKClient instance."""
        client = get_jwk_client()
        assert client is not None
        assert isinstance(client, jwt.PyJWKClient)

    def test_get_jwk_client_uses_correct_url(self):
        """Test that get_jwk_client constructs the correct JWKS URL."""
        with patch("src.auth.settings") as mock_settings:
            mock_settings.better_auth_url = "http://test.example.com"
            # Clear cache to ensure new client is created
            get_jwk_client.cache_clear()
            client = get_jwk_client()
            # Verify the URL was constructed correctly
            assert client.uri == "http://test.example.com/api/auth/jwks"

    def test_get_jwk_client_is_cached(self):
        """Test that get_jwk_client caches the client instance."""
        get_jwk_client.cache_clear()
        client1 = get_jwk_client()
        client2 = get_jwk_client()
        assert client1 is client2  # Same instance due to lru_cache


class TestGetCurrentUser:
    """Tests for JWT verification and user extraction."""

    @pytest.mark.asyncio
    async def test_valid_token_returns_user_id(self):
        """Test that a valid JWT returns the user ID from sub claim."""
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="valid.jwt.token"
        )

        # Mock the JWKS client and JWT decoding
        with patch("src.auth.get_jwk_client") as mock_get_client:
            mock_jwk_client = Mock()
            mock_signing_key = Mock()
            mock_signing_key.key = "mock_key"
            mock_jwk_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_get_client.return_value = mock_jwk_client

            with patch("src.auth.jwt.decode") as mock_decode:
                mock_decode.return_value = {"sub": "user123"}

                user_id = await get_current_user(mock_credentials)

                assert user_id == "user123"
                mock_jwk_client.get_signing_key_from_jwt.assert_called_once_with(
                    "valid.jwt.token"
                )
                mock_decode.assert_called_once()

    @pytest.mark.asyncio
    async def test_token_without_sub_claim_raises_401(self):
        """Test that a token without 'sub' claim raises 401."""
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid.jwt.token"
        )

        with patch("src.auth.get_jwk_client") as mock_get_client:
            mock_jwk_client = Mock()
            mock_signing_key = Mock()
            mock_signing_key.key = "mock_key"
            mock_jwk_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_get_client.return_value = mock_jwk_client

            with patch("src.auth.jwt.decode") as mock_decode:
                # Token without 'sub' claim
                mock_decode.return_value = {"other": "data"}

                with pytest.raises(HTTPException) as exc_info:
                    await get_current_user(mock_credentials)

                assert exc_info.value.status_code == 401
                assert "missing user ID" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_invalid_jwt_signature_raises_401(self):
        """Test that an invalid JWT signature raises 401."""
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid.signature.token"
        )

        with patch("src.auth.get_jwk_client") as mock_get_client:
            mock_jwk_client = Mock()
            mock_signing_key = Mock()
            mock_signing_key.key = "mock_key"
            mock_jwk_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_get_client.return_value = mock_jwk_client

            with patch("src.auth.jwt.decode") as mock_decode:
                # Simulate JWT signature verification failure
                mock_decode.side_effect = jwt.exceptions.InvalidSignatureError(
                    "Signature verification failed"
                )

                with pytest.raises(HTTPException) as exc_info:
                    await get_current_user(mock_credentials)

                assert exc_info.value.status_code == 401
                assert "Invalid token" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_expired_token_raises_401(self):
        """Test that an expired JWT raises 401."""
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="expired.jwt.token"
        )

        with patch("src.auth.get_jwk_client") as mock_get_client:
            mock_jwk_client = Mock()
            mock_signing_key = Mock()
            mock_signing_key.key = "mock_key"
            mock_jwk_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_get_client.return_value = mock_jwk_client

            with patch("src.auth.jwt.decode") as mock_decode:
                # Simulate expired token
                mock_decode.side_effect = jwt.exceptions.ExpiredSignatureError(
                    "Token has expired"
                )

                with pytest.raises(HTTPException) as exc_info:
                    await get_current_user(mock_credentials)

                assert exc_info.value.status_code == 401
                assert "Invalid token" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_malformed_token_raises_401(self):
        """Test that a malformed JWT raises 401."""
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="malformed.token"
        )

        with patch("src.auth.get_jwk_client") as mock_get_client:
            mock_jwk_client = Mock()
            mock_signing_key = Mock()
            mock_signing_key.key = "mock_key"
            mock_jwk_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_get_client.return_value = mock_jwk_client

            with patch("src.auth.jwt.decode") as mock_decode:
                # Simulate malformed token
                mock_decode.side_effect = jwt.exceptions.DecodeError(
                    "Not enough segments"
                )

                with pytest.raises(HTTPException) as exc_info:
                    await get_current_user(mock_credentials)

                assert exc_info.value.status_code == 401
                assert "Invalid token" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_jwt_decode_uses_rs256_algorithm(self):
        """Test that JWT decoding uses RS256 algorithm."""
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="test.jwt.token"
        )

        with patch("src.auth.get_jwk_client") as mock_get_client:
            mock_jwk_client = Mock()
            mock_signing_key = Mock()
            mock_signing_key.key = "mock_key"
            mock_jwk_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_get_client.return_value = mock_jwk_client

            with patch("src.auth.jwt.decode") as mock_decode:
                mock_decode.return_value = {"sub": "user456"}

                await get_current_user(mock_credentials)

                # Verify RS256 algorithm is used
                call_kwargs = mock_decode.call_args[1]
                assert "RS256" in call_kwargs["algorithms"]

    @pytest.mark.asyncio
    async def test_jwt_decode_disables_audience_verification(self):
        """Test that JWT decoding disables audience verification."""
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="test.jwt.token"
        )

        with patch("src.auth.get_jwk_client") as mock_get_client:
            mock_jwk_client = Mock()
            mock_signing_key = Mock()
            mock_signing_key.key = "mock_key"
            mock_jwk_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_get_client.return_value = mock_jwk_client

            with patch("src.auth.jwt.decode") as mock_decode:
                mock_decode.return_value = {"sub": "user789"}

                await get_current_user(mock_credentials)

                # Verify audience verification is disabled
                call_kwargs = mock_decode.call_args[1]
                assert call_kwargs["options"]["verify_aud"] is False
