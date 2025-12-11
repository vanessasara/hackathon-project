"""
Push Subscription CRUD endpoints for the API.

Part B: Advanced Features - Browser Push Notifications

This module provides endpoints for managing browser push notification
subscriptions. Users register their browser subscriptions to receive
task reminder notifications even when the browser tab is closed.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..auth import get_current_user
from ..database import get_session
from ..models.push_subscription import PushSubscription
from ..schemas.push_subscription import (
    PushSubscriptionCreate,
    PushSubscriptionResponse,
    PushSubscriptionDelete,
)

router = APIRouter(prefix="/push-subscriptions", tags=["push-subscriptions"])


@router.get("", response_model=List[PushSubscriptionResponse])
async def list_push_subscriptions(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[PushSubscriptionResponse]:
    """
    List all push subscriptions for the authenticated user.

    Args:
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        List[PushSubscriptionResponse]: User's push subscriptions
    """
    statement = select(PushSubscription).where(PushSubscription.user_id == user_id)
    result = await session.execute(statement)
    subscriptions = result.scalars().all()
    return [PushSubscriptionResponse.model_validate(sub) for sub in subscriptions]


@router.post("", response_model=PushSubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_push_subscription(
    subscription_data: PushSubscriptionCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> PushSubscriptionResponse:
    """
    Register a browser push subscription.

    If a subscription with the same endpoint already exists for this user,
    it will be updated with the new keys.

    Args:
        subscription_data: Push subscription data from browser
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        PushSubscriptionResponse: The created or updated subscription
    """
    # Check if subscription with this endpoint already exists for user
    statement = select(PushSubscription).where(
        PushSubscription.user_id == user_id,
        PushSubscription.endpoint == subscription_data.endpoint,
    )
    result = await session.execute(statement)
    existing = result.scalar_one_or_none()

    if existing:
        # Update existing subscription with new keys
        existing.p256dh_key = subscription_data.p256dh_key
        existing.auth_key = subscription_data.auth_key
        existing.user_agent = subscription_data.user_agent
        existing.mark_updated()
        session.add(existing)
        await session.commit()
        await session.refresh(existing)
        return PushSubscriptionResponse.model_validate(existing)

    # Create new subscription
    subscription = PushSubscription(
        user_id=user_id,
        endpoint=subscription_data.endpoint,
        p256dh_key=subscription_data.p256dh_key,
        auth_key=subscription_data.auth_key,
        user_agent=subscription_data.user_agent,
    )
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    return PushSubscriptionResponse.model_validate(subscription)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_push_subscription(
    subscription_data: PushSubscriptionDelete,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Remove a browser push subscription.

    Called when the user logs out or revokes notification permission.

    Args:
        subscription_data: Contains the endpoint to delete
        user_id: User ID extracted from JWT token
        session: Database session
    """
    statement = select(PushSubscription).where(
        PushSubscription.user_id == user_id,
        PushSubscription.endpoint == subscription_data.endpoint,
    )
    result = await session.execute(statement)
    subscription = result.scalar_one_or_none()

    if subscription:
        await session.delete(subscription)
        await session.commit()


@router.delete("/all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_push_subscriptions(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Remove all push subscriptions for the authenticated user.

    Called when the user wants to disable all notifications.

    Args:
        user_id: User ID extracted from JWT token
        session: Database session
    """
    statement = select(PushSubscription).where(PushSubscription.user_id == user_id)
    result = await session.execute(statement)
    subscriptions = result.scalars().all()

    for subscription in subscriptions:
        await session.delete(subscription)

    await session.commit()
