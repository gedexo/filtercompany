from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class Banner(models.Model):
    BANNER_CHOICES = [
    ('mobile','Mobile'),
    ('system','System'),
    ]
    size = models.CharField(max_length=128,choices=BANNER_CHOICES,blank=True, null=True,default='system')
    product = models.ForeignKey("web.Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="banner-images/")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        
    def __str__(self):
        return self.name
    
    def get_product_detail_url(self):
        return reverse('web:product_details', kwargs={'slug': self.product.slug})
    
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=120, blank=True)
    image = models.ImageField(upload_to="product-categories/", blank=True, null=True)
    description = HTMLField(blank=True, null=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("web:products_by_category", kwargs={"slug": self.slug})


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products",
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    image = models.ImageField(upload_to="products/")
    size = models.CharField(max_length=120, blank=True, null=True)
    price = models.CharField(max_length=120, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    description =HTMLField()
    #meta
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description=models.TextField(blank=True, null=True)
    schema_description=models.TextField(blank=True, null=True)
    key_word=models.TextField(blank=True, null=True)
    canonical_URL=models.URLField(max_length=200,blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse("web:product_details", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class ProductEnquiry(models.Model):
    product = models.ForeignKey("web.Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=120)
    message = models.CharField(max_length=900)

    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = "Product Enquiry"
        verbose_name_plural = "Product Enquiries"

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    position = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="testimonial-images",
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return str(self.name)


class Blog(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    keyword = models.TextField( blank=True, null=True)
    meta_title = models.CharField(max_length=225, blank=True, null=True)
    meta_description = models.CharField(max_length=225, blank=True, null=True)
    canonical = models.URLField(max_length=200,blank=True, null=True)
    image = models.ImageField(
        upload_to="blog-images/",
    )
    content = HTMLField()
    date = models.DateField()

    def get_absolute_url(self):
        return reverse("web:blog-details", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return str(self.title)


class Contact(models.Model):
    name = models.CharField(max_length=120)
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=120, blank=True, null=True)
    subject = models.CharField(max_length=120, blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return str(self.name)


class Enquiry(models.Model):
    service = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return str(self.name)


class Logo(models.Model):
    image = models.ImageField(upload_to='partner_logos/')

    def __str__(self):
        return str(self.image)


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return str(self.question)


class IframeLink(models.Model):
    link = models.TextField(help_text="Paste the full iframe embed link or long URL here")

    class Meta:
        verbose_name = "Iframe Link"
        verbose_name_plural = "Iframe Link"

    def __str__(self):
        return self.link
