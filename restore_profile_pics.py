from pathlib import Path

from image_utils import upload_profile_image

import asyncio
import boto3

from config import settings


async def main():
    folder = Path("media/profile_pics")

    s3 = boto3.client(
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

    bucket = settings.s3_bucket_name
    restored = 0
    skipped = 0

    for path in folder.iterdir():
        if not path.is_file() or path.name == "corey.png":
            continue

        key = f"profile_pics/{path.name}"

        try:
            s3.head_object(Bucket=bucket, Key=key)
            print(f"Уже существует: {path.name}")
            skipped += 1
            continue
        except s3.exceptions.ClientError as error:
            code = error.response["Error"]["Code"]
            if code not in ("404", "NoSuchKey", "NotFound"):
                print(f"Ошибка проверки {path.name}: {error}")
                continue

        try:
            await upload_profile_image(path.read_bytes(), path.name)
            print(f"Восстановлено: {path.name}")
            restored += 1
        except Exception as error:
            print(f"Ошибка загрузки {path.name}: {error}")

    print(f"\nГотово. Восстановлено: {restored}, уже существовало: {skipped}")


if __name__ == "__main__":
    asyncio.run(main())