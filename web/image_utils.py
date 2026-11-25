"""Convert uploaded images to WebP, as high quality as possible while staying under a size limit."""

import io

from PIL import Image, ImageOps

MAX_BYTES = 70 * 1024  # 70 KB target
MAX_DIMENSION = 1920  # never store anything wider/taller than this
MIN_DIMENSION = 320  # don't shrink below this when chasing the size limit
MIN_QUALITY = 45  # below this, shrink dimensions instead of lowering quality further
MAX_QUALITY = 90


def _encode(img, quality):
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=quality, method=6)
    return buf.getvalue()


def _best_quality_under_limit(img, max_bytes):
    """Binary-search the highest quality whose output fits; returns bytes or None."""
    lo, hi, best = MIN_QUALITY, MAX_QUALITY, None
    while lo <= hi:
        q = (lo + hi) // 2
        data = _encode(img, q)
        if len(data) <= max_bytes:
            best = data
            lo = q + 1
        else:
            hi = q - 1
    return best


def compress_to_webp(file_obj, max_bytes=MAX_BYTES):
    """Return WebP bytes for the given image file, aiming for <= max_bytes."""
    file_obj.seek(0)
    img = Image.open(file_obj)
    img = ImageOps.exif_transpose(img)  # respect phone camera rotation

    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    img = img.convert("RGBA" if has_alpha else "RGB")

    img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)

    while True:
        data = _best_quality_under_limit(img, max_bytes)
        if data is not None:
            return data
        w, h = img.size
        if max(w, h) <= MIN_DIMENSION:
            # Can't shrink further: return the smallest acceptable-quality version.
            return _encode(img, MIN_QUALITY)
        img = img.resize((max(1, int(w * 0.85)), max(1, int(h * 0.85))), Image.LANCZOS)

