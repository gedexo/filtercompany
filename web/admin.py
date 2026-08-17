from django.contrib import admin

from .models import Blog, Contact, Enquiry, Product, ProductCategory, ProductEnquiry, Testimonial,Logo, Banner, Faq,IframeLink
from django.utils.safestring import mark_safe

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "product",
        "size",
    )
    list_filter = ("size",)
    autocomplete_fields = ["product"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "size",
        "price",
        "is_active",
    )
    search_fields = ["name"]
    list_filter = ("category", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["category"]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "image_preview")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:cover;border-radius:6px;">'
            )
        return "-"

    image_preview.short_description = "Image"


@admin.register(ProductEnquiry)
class ProductEnquiryAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "email", "phone","timestamp")


# @admin.register(Testimonial)
# class TestimonialAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "position",
#     )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "timestamp"
    )


# @admin.register(Enquiry)
# class EnquiryForm(admin.ModelAdmin):
#     list_display = ("name", "email", "message")


# @admin.register(Logo)
# class LogoAdmin(admin.ModelAdmin):
#     list_display =(
#         "image",
#     )

#     def image_preview(self, obj):
#         if obj.image:
#             return mark_safe(
#                 f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
#             )
#         return None

#     image_preview.short_description = "Image Preview"


# @admin.register(Faq)
# class FaqAdmin(admin.ModelAdmin):
#     list_display = ("question", "answer")


# @admin.register(IframeLink)
# class IframeLinkAdmin(admin.ModelAdmin):
#     list_display = ('id',)
