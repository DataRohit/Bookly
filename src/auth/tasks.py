import asyncio

import celery

from pkg.db import get_session
from src.auth.service import PasswordResetLogService, TokenBlackListService


@celery.shared_task
def clear_expired_blacklisted_tokens_task():
    async def async_clear_expired_tokens():
        async for session in get_session():
            token_blacklist_service = TokenBlackListService()
            await token_blacklist_service.clear_expired_blacklisted_tokens(session)

    asyncio.run(async_clear_expired_tokens())


@celery.shared_task
def clear_password_reset_logs_task():
    async def async_clear_password_reset_logs():
        async for session in get_session():
            password_reset_log_service = PasswordResetLogService()
            await password_reset_log_service.clear_password_reset_logs(session)

    asyncio.run(async_clear_password_reset_logs())
