from minio import Minio

from .config import Config

minio_client = Minio(
    endpoint=Config.MINIO_STORAGE_ENDPOINT,
    access_key=Config.MINIO_ACCESS_KEY,
    secret_key=Config.MINIO_SECRET_KEY,
    secure=False,
)

if not minio_client.bucket_exists(Config.MINIO_STORAGE_BUCKET):
    minio_client.make_bucket(Config.MINIO_STORAGE_BUCKET)
    print(f"Bucket {Config.MINIO_STORAGE_BUCKET} created")
