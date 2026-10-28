import uuid
from io import BytesIO
from pathlib import Path
import boto3
from PIL import Image, ImageOps
from config import settings
from starlette.concurrency import run_in_threadpool 



PROFILE_PICS_DIR = Path("media/profile_pics")


def save_profile_image_locally(file_bytes: bytes, filename: str) -> None:
    """Сохраняет байты изображения в локальную папку."""
    PROFILE_PICS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = PROFILE_PICS_DIR / filename
    with open(filepath, "wb") as f:
        f.write(file_bytes)


def _get_s3_client():
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


def process_profile_image(content: bytes) -> tuple[bytes, str]:

    """Принимает байты изображения, сжимает до 300x300 и конвертирует в JPEG."""

    with Image.open(BytesIO(content)) as original:

        img = ImageOps.exif_transpose(original)

        img = ImageOps.fit(

            img,

            (300, 300),

            method=Image.Resampling.LANCZOS,

        )

        if img.mode != "RGB":

            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"

        output = BytesIO()

        img.save(output, format="JPEG", quality=85, optimize=True)

        return output.getvalue(), filename

def _upload_to_s3(file_bytes: bytes, key: str) -> None:
    s3 = _get_s3_client()

    print("S3 BUCKET:", settings.s3_bucket_name)
    print("S3 KEY:", key)

    s3.upload_fileobj(
        BytesIO(file_bytes),
        settings.s3_bucket_name,
        key,
        ExtraArgs={"ContentType": "image/jpeg"},
    )


def _delete_from_s3(key: str) -> None:
    s3 = _get_s3_client()
    s3.delete_object(Bucket=settings.s3_bucket_name, Key=key)


async def upload_profile_image(file_bytes: bytes, filename: str) -> None:
    key = f"profile_pics/{filename}"
    await run_in_threadpool(_upload_to_s3, file_bytes, key)


async def delete_profile_image(filename: str | None) -> None:
    if filename is None:
        return
    key = f"profile_pics/{filename}"
    await run_in_threadpool(_delete_from_s3, key)