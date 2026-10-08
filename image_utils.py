import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

PROFILE_PICS_DIR = Path("media/profile_pics")


def process_profile_image(content: bytes) -> str:
    """Принимает байты изображения, сжимает до 300x300, конвертирует в JPEG и сохраняет."""
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)

        img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = PROFILE_PICS_DIR / filename

        PROFILE_PICS_DIR.mkdir(parents=True, exist_ok=True)

        img.save(filepath, "JPEG", quality=85, optimize=True)

    return filename


def delete_profile_image(filename: str | None) -> None:
    """Удаляет файл аватара с диска, если он существует."""
    if filename is None:
        return

    filepath = PROFILE_PICS_DIR / filename
    if filepath.exists():
        filepath.unlink()


def create_default_avatar() -> str:
    """Генерирует дефолтную тестовую аватарку (используется при сидинге БД)."""
    img = Image.new("RGB", (300, 300), color=(70, 130, 180))
    buf = BytesIO()
    img.save(buf, format="JPEG")
    return process_profile_image(buf.getvalue())