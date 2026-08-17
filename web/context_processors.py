from django.conf import settings

from .models import Product, ProductCategory

def products(request):
    return {
        'all_products': Product.objects.filter(is_active=True)[:6],
        'product_categories': ProductCategory.objects.prefetch_related('products').order_by('id'),
    }


def turnstile(request):
    return {
        "cf_turnstile_site_key": settings.CF_TURNSTILE_SITE_KEY,
        "static_asset_version": settings.STATIC_ASSET_VERSION,
    }
