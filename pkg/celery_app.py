from celery import Celery

from .config import Config

celery_app = Celery("bookly", broker=Config.REDIS_URL, backend=Config.REDIS_URL)
celery_app.config_from_object(Config, namespace="CELERY")
celery_app.autodiscover_tasks(["pkg.tasks"])
