#!/usr/bin/env python3
"""
Generate VAPID keys for Web Push notifications.

Part B: Advanced Features - Notifications

Run this script once to generate VAPID keys, then store them
as Kubernetes secrets for production use.

Usage:
    python generate_vapid.py

Output:
    VAPID_PUBLIC_KEY and VAPID_PRIVATE_KEY values to add to your secrets.
"""

import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


def main():
    """Generate and print VAPID keys."""
    print("Generating VAPID keys for Web Push notifications...\n")

    # Generate ECDSA key pair using P-256 curve (required for Web Push VAPID)
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    # Get raw key bytes
    private_bytes = private_key.private_numbers().private_value.to_bytes(32, 'big')
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    # Convert to URL-safe base64 format (no padding) used by Web Push
    def to_base64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode().rstrip("=")

    public_key_b64 = to_base64url(public_bytes)
    private_key_b64 = to_base64url(private_bytes)

    print("=" * 60)
    print("VAPID Keys Generated Successfully!")
    print("=" * 60)
    print()
    print("Add these to your environment variables or Kubernetes secrets:")
    print()
    print(f"VAPID_PUBLIC_KEY={public_key_b64}")
    print()
    print(f"VAPID_PRIVATE_KEY={private_key_b64}")
    print()
    print("=" * 60)
    print()
    print("For Helm deployment, add to values-doks.yaml secrets:")
    print()
    print("secrets:")
    print(f'  VAPID_PUBLIC_KEY: "{public_key_b64}"')
    print(f'  VAPID_PRIVATE_KEY: "{private_key_b64}"')
    print()
    print("For frontend, add VAPID_PUBLIC_KEY to NEXT_PUBLIC_VAPID_PUBLIC_KEY")


if __name__ == "__main__":
    main()
