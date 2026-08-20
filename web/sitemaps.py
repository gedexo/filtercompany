from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Blog, Product, ProductCategory


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return ["web:index", "web:about", "web:products", "web:contact"]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(is_active=True).exclude(slug="")

    def location(self, item):
        return item.get_absolute_url()


class CategorySitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return ProductCategory.objects.exclude(slug="")

    def location(self, item):
        return item.get_absolute_url()


class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Blog.objects.exclude(slug="")

    def location(self, item):
        return item.get_absolute_url()

    def lastmod(self, item):
        return item.date
