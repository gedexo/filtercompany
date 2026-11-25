import logging

from django.core.files.base import ContentFile
from django.db.models import ImageField
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .image_utils import MAX_BYTES, compress_to_webp, webp_name

logger = logging.getLogger(__name__)


@receiver(pre_save)
def convert_uploaded_images_to_webp(sender, instance, **kwargs):
    """Convert every newly uploaded image on models in the `web` app to WebP under 70 KB."""
    if sender._meta.app_label != "web" or kwargs.get("raw"):
        return

    for field in sender._meta.get_fields():
        if not isinstance(field, ImageField):
            continue

        field_file = getattr(instance, field.attname)
        # Only touch files that were just uploaded and not yet written to storage.
        if not field_file or getattr(field_file, "_committed", True):
            continue

        name = field_file.name or ""
        try:
            # Already a small WebP: keep as-is.
            if name.lower().endswith(".webp") and field_file.size <= MAX_BYTES:
                continue
            data = compress_to_webp(field_file.file)
        except Exception:  # unreadable / unsupported image: keep the original upload
            logger.exception("WebP conversion failed for %s.%s", sender.__name__, field.name)
            continue

        field_file.save(webp_name(name), ContentFile(data), save=False)
