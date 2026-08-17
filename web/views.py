import json
from urllib.parse import quote
from urllib import parse, request as urllib_request
from urllib.error import URLError

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from web.forms import ContactForm, ProductEnquiryForm

from .models import Blog, Product, ProductCategory, Testimonial,Logo, Banner, Faq,IframeLink

WHATSAPP_NUMBER = "919895875100"


def whatsapp_redirect(message):
    return redirect(f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}")


def verify_turnstile(request):
    token = request.POST.get("cf-turnstile-response")
    if not token:
        return False

    payload = parse.urlencode(
        {
            "secret": settings.CF_TURNSTILE_SECRET_KEY,
            "response": token,
            "remoteip": request.META.get("REMOTE_ADDR", ""),
        }
    ).encode()
    req = urllib_request.Request(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data=payload,
        method="POST",
    )

    try:
        with urllib_request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return False

    return bool(result.get("success"))

def index(request):
    mobile = Banner.objects.filter(size="mobile")
    system = Banner.objects.filter(size="system")
    products = Product.objects.filter(is_active=True)[:6]
    blogs = Blog.objects.all()
    testimonial = Testimonial.objects.all()
    logos = Logo.objects.all()
    faqs = Faq.objects.all()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            if not verify_turnstile(request):
                form.add_error(None, "Turnstile verification failed. Please try again.")
            else:
                data = form.save()
                message = (
                    "New contact enquiry from website\n"
                    f"Name: {data.name}\n"
                    f"Phone: {data.phone or 'N/A'}\n"
                    f"Subject: {data.subject or 'N/A'}\n"
                    f"Message: {data.message}"
                )
                return whatsapp_redirect(message)
        else:
            print(form.errors)
    else:
        form = ContactForm()

    context = {
        "is_index": True,
        "mobile": mobile,
        "system": system,
        "products": products,
        "testimonial": testimonial,
        "blogs": blogs,
        "form": form,
        "logos": logos,
        "faqs":faqs
    }
    return render(request, "web/index.html", context)


def about(request):
    testimonial = Testimonial.objects.all()
    context = {"is_about": True,
               "testimonial": testimonial}
    return render(request, "web/about.html", context)

def products(request):
    products = Product.objects.select_related("category").filter(is_active=True)
    context = {"is_products": True, "products": products, "category": None}
    return render(request, "web/products.html", context)


def products_by_category(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    products = Product.objects.select_related("category").filter(category=category, is_active=True)
    context = {"is_products": True, "products": products, "category": category}
    return render(request, "web/products.html", context)


def product_details(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug, is_active=True)
    other_products = Product.objects.filter(is_active=True).exclude(slug=slug)

    form = ProductEnquiryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            if not verify_turnstile(request):
                form.add_error(None, "Turnstile verification failed. Please try again.")
            else:
                data = form.save(commit=False)
                data.product = product
                data.save()
                message = (
                    "New product enquiry from website\n"
                    f"Product: {product.name}\n"
                    f"Name: {data.name}\n"
                    f"Phone: {data.phone or 'N/A'}\n"
                    f"Message: {data.message}"
                )
                return whatsapp_redirect(message)
        print(form.errors)

    context = {
        "is_products": True,
        "product": product,
        "other_products": other_products,
        "form": form,
    }
    return render(request, "web/product-details.html", context)


def blog(request):
    blogs = Blog.objects.all()

    context = {"is_blog": True, "blogs": blogs}
    return render(request, "web/blog.html", context)


def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    context = {
        "blog": blog,
    }

    return render(request, "web/blog-details.html", context)


def contact(request):
    form = ContactForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            if not verify_turnstile(request):
                form.add_error(None, "Turnstile verification failed. Please try again.")
            else:
                data = form.save()
                message = (
                    "New contact enquiry from website\n"
                    f"Name: {data.name}\n"
                    f"Phone: {data.phone or 'N/A'}\n"
                    f"Subject: {data.subject or 'N/A'}\n"
                    f"Message: {data.message}"
                )
                return whatsapp_redirect(message)
        else:
            print(form.errors)
    else:
        form = ContactForm()
    context = {
        "form": form,
    }
    return render(request, "web/contact.html", context)


def iframe_view(request):
    iframe = IframeLink.objects.last()
    return render(request, "web/PET/index.html", {"iframe": iframe})
