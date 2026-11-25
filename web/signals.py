import logging
import os

from django.core.files.base import ContentFile
from django.db.models import ImageField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .image_utils import MAX_BYTES, compress_to_webp

logger = logging.getLogger(__name__)

MAX_NAME_LENGTH = 80


def _upload_file_name(instance, original_name):
    """SEO file name: alt text -> title / name -> original file name, slugified, as .webp."""
    label = instance.image_label() if hasattr(instance, "image_label") else ""
    if not label:
        label = os.path.splitext(os.path.basename(original_name))[0]
    base = slugify(label)[:MAX_NAME_LENGTH].strip("-") or "image"
    return f"{base}.webp"


@receiver(pre_save)
def convert_uploaded_images_to_webp(sender, instance, **kwargs):
    """For every newly uploaded image on `web` models: convert to WebP under 70 KB and
    name the file after its alt text (or title / name, or the original file name)."""
    if sender._meta.app_label != "web" or kwargs.get("raw"):
        return

    for field in sender._meta.get_fields():
        if not isinstance(field, ImageField):
            continue

        field_file = getattr(instance, field.attname)
        # Only touch files that were just uploaded and not yet written to storage.
        if not field_file or getattr(field_file, "_committed", True):
            continue

        original_name = field_file.name or ""
        new_name = _upload_file_name(instance, original_name)
        try:
            if original_name.lower().endswith(".webp") and field_file.size <= MAX_BYTES:
                field_file.file.seek(0)
                data = field_file.file.read()  # already a small WebP: just rename
            else:
                data = compress_to_webp(field_file.file)
        except Exception:  # unreadable / unsupported image: keep the original upload
            logger.exception("WebP conversion failed for %s.%s", sender.__name__, field.name)
            continue

        field_file.save(new_name, ContentFile(data), save=False)
