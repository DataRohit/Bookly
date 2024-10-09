from datetime import timedelta

from celery import Celery

from .config import Config

celery_app = Celery("bookly", broker=Config.REDIS_URL, backend=Config.REDIS_URL)
celery_app.config_from_object(Config, namespace="CELERY")
celery_app.autodiscover_tasks(["pkg.tasks", "src.auth.tasks"])

celery_app.conf.beat_schedule = {
    "clear-expired-blacklisted-tokens-task": {
        "task": "src.auth.tasks.clear_expired_blacklisted_tokens_task",
        "schedule": timedelta(hours=1),
    },
    "clear-password-reset-logs-task": {
        "task": "src.auth.tasks.clear_password_reset_logs_task",
        "schedule": timedelta(hours=6),
    },
}
