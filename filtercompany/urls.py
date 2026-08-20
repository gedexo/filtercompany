from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from web.sitemaps import BlogSitemap, CategorySitemap, ProductSitemap, StaticViewSitemap

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("web.urls", namespace="web")),
        path(
            "sitemap.xml",
            sitemap,
            {
                "sitemaps": {
                    "static": StaticViewSitemap,
                    "products": ProductSitemap,
                    "categories": CategorySitemap,
                    "blogs": BlogSitemap,
                }
            },
            name="sitemap",
        ),
        path(
            "robots.txt",
            TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.site_header = "filtercompany Administration"
admin.site.site_title = "filtercompany Admin Portal"
admin.site.index_title = "Welcome to filtercompany Admin Portal"
