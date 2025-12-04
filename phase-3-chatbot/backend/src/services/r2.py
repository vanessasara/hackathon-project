"""Cloudflare R2 storage service for image uploads."""

import boto3
from botocore.exceptions import ClientError

from src.config import settings


class R2Service:
    """Service for interacting with Cloudflare R2 storage."""

    def __init__(self):
        """Initialize R2 client with credentials from settings."""
        self._client = None

    @property
    def client(self):
        """Lazy initialization of boto3 S3 client for R2."""
        if self._client is None:
            if not settings.r2_account_id:
                raise ValueError("R2_ACCOUNT_ID is not configured")

            self._client = boto3.client(
                "s3",
                endpoint_url=f"https://{settings.r2_account_id}.r2.cloudflarestorage.com",
                aws_access_key_id=settings.r2_access_key_id,
                aws_secret_access_key=settings.r2_secret_access_key,
                region_name="auto",
            )
        return self._client

    def upload(self, file_bytes: bytes, key: str, content_type: str) -> str:
        """
        Upload a file to R2 storage.

        Args:
            file_bytes: The file content as bytes
            key: The object key (path) in the bucket
            content_type: MIME type of the file

        Returns:
            The public URL of the uploaded file

        Raises:
            ClientError: If the upload fails
        """
        self.client.put_object(
            Bucket=settings.r2_bucket_name,
            Key=key,
            Body=file_bytes,
            ContentType=content_type,
        )
        return f"{settings.r2_public_url}/{key}"

    def delete(self, key: str) -> bool:
        """
        Delete a file from R2 storage.

        Args:
            key: The object key (path) in the bucket

        Returns:
            True if deletion was successful

        Raises:
            ClientError: If the deletion fails
        """
        try:
            self.client.delete_object(
                Bucket=settings.r2_bucket_name,
                Key=key,
            )
            return True
        except ClientError:
            return False


# Singleton instance
r2_service = R2Service()
