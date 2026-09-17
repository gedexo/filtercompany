from django.conf import settings
from .models import Blog, MetaTag, Product, ProductCategory

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


def seo_meta(request):
    url_name = getattr(request.resolver_match, "url_name", "") if hasattr(request, "resolver_match") and request.resolver_match else ""
    kwargs = getattr(request.resolver_match, "kwargs", {}) if hasattr(request, "resolver_match") and request.resolver_match else {}

    default_title = "The Filter Company | Advanced Water Purification & Filtration Solutions"
    default_desc = "The Filter Company provides advanced water purification and filtration solutions including RO, UV, UF, and mineral enrichment systems for homes, businesses, and industries."
    default_keywords = "water purification, water purifier, RO water purifier, UV water purification, UF filtration, water filtration systems, water treatment solutions, domestic water purifier, commercial water purifier, industrial water purification, mineral enrichment"

    meta_title = None
    meta_description = None
    keywords = None
    canonical_url = None
    schema_description = None
    og_title = None
    og_description = None
    og_image = None

    if url_name == "product_details":
        slug = kwargs.get("slug")
        if slug:
            try:
                product = Product.objects.filter(slug=slug).first()
                if product:
                    meta_title = product.meta_title
                    meta_description = product.meta_description
                    keywords = product.key_word
                    canonical_url = product.canonical_URL
                    schema_description = product.schema_description
                    if product.image:
                        og_image = product.image.url
            except Exception:
                pass
    elif url_name == "blog-details":
        slug = kwargs.get("slug")
        if slug:
            try:
                blog_obj = Blog.objects.filter(slug=slug).first()
                if blog_obj:
                    meta_title = blog_obj.meta_title
                    meta_description = blog_obj.meta_description
                    keywords = blog_obj.keyword
                    canonical_url = blog_obj.canonical
                    if blog_obj.image:
                        og_image = blog_obj.image.url
            except Exception:
                pass
    else:
        PAGE_MAP = {
            "index": "home",
            "about": "about",
            "products": "products",
            "products_by_category": "products",
            "blog": "blog",
            "contact": "contact",
        }
        page_key = PAGE_MAP.get(url_name, "")
        if page_key:
            try:
                page_meta = MetaTag.objects.filter(page=page_key).first()
                if page_meta:
                    meta_title = page_meta.meta_title
                    meta_description = page_meta.meta_description
                    keywords = page_meta.keywords
                    canonical_url = page_meta.canonical_url
                    schema_description = page_meta.schema_description
                    og_title = page_meta.og_title
                    og_description = page_meta.og_description
                    if page_meta.og_image:
                        og_image = page_meta.og_image.url
            except Exception:
                pass

    final_title = meta_title if meta_title else default_title
    final_desc = meta_description if meta_description else default_desc
    final_keywords = keywords if keywords else default_keywords

    meta = {
        "meta_title": final_title,
        "meta_description": final_desc,
        "keywords": final_keywords,
        "canonical_url": canonical_url if canonical_url else "",
        "schema_description": schema_description if schema_description else "",
        "og_title": og_title if og_title else final_title,
        "og_description": og_description if og_description else final_desc,
        "og_image": og_image if og_image else "",
    }

    return {"seo_meta": meta}


