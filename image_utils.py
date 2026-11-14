import uuid
from io import BytesIO

import boto3
from botocore.exceptions import ClientError
from PIL import Image, ImageOps

from config import settings


def process_profile_image(content: bytes) -> tuple[bytes, str]:
    """
    Принимает байты изображения, сжимает до 300x300,
    конвертирует в JPEG и возвращает (байты, имя_файла).
    """
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)
        img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        output = BytesIO()
        img.save(output, format="JPEG", quality=85, optimize=True)
        
        filename = f"{uuid.uuid4().hex}.jpg"
        return output.getvalue(), filename


def _get_s3_client():
    """Создает клиент S3 с настройками из config."""
    return boto3.client(
        "s3",
        region_name=settings.s3_region,
        aws_access_key_id=(
            settings.s3_access_key_id.get_secret_value()
            if settings.s3_access_key_id
            else None
        ),
        aws_secret_access_key=(
            settings.s3_secret_access_key.get_secret_value()
            if settings.s3_secret_access_key
            else None
        ),
        endpoint_url=settings.s3_endpoint_url,
    )


def _upload_to_s3(file_bytes: bytes, key: str) -> None:
    """Загружает файл в S3."""
    s3 = _get_s3_client()
    s3.upload_fileobj(
        BytesIO(file_bytes),
        settings.s3_bucket_name,
        key,
        ExtraArgs={"ContentType": "image/jpeg"},
    )


def _delete_from_s3(key: str) -> None:
    """Удаляет файл из S3."""
    s3 = _get_s3_client()
    s3.delete_object(Bucket=settings.s3_bucket_name, Key=key)


async def upload_profile_image(file_bytes: bytes, filename: str) -> None:
    """Асинхронная обертка для загрузки (через threadpool)."""
    import anyio
    key = f"profile_pics/{filename}"
    await anyio.to_thread.run_sync(_upload_to_s3, file_bytes, key)


async def delete_profile_image(filename: str | None) -> None:
    """Асинхронная обертка для удаления."""
    if filename is None:
        return
    import anyio
    key = f"profile_pics/{filename}"
    await anyio.to_thread.run_sync(_delete_from_s3, key)