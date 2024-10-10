from io import BytesIO

from pkg.celery_app import celery_app
from pkg.config import Config
from pkg.storage import minio_client


@celery_app.task
def upload_user_avatar_image_task(
    image_content: bytes, filename: str, content_type: str
):
    file_data = BytesIO(image_content)

    minio_client.put_object(
        bucket_name=Config.MINIO_STORAGE_BUCKET,
        object_name=filename,
        data=file_data,
        length=len(image_content),
        content_type=content_type,
    )
