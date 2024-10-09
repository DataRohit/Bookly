from asgiref.sync import async_to_sync

from pkg.celery_app import celery_app
from pkg.mail import send_email


@celery_app.task
def send_email_task(
    recipients: list[str], subject: str, template_name: str, context: dict
):
    async_to_sync(send_email)(recipients, subject, template_name, context)
