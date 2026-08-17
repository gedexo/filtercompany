from django import forms
from django.forms import widgets

from .models import Contact, Enquiry, Product, ProductEnquiry


class ProductEnquiryForm(forms.ModelForm):
    class Meta:
        model = ProductEnquiry
        fields = ["name", "phone", "message"]
        widgets = {
            "name": widgets.TextInput(
                attrs={"class": "required form-control", "placeholder": "Your Name"}
            ),
            "phone": widgets.TextInput(
                attrs={"class": "required form-control", "placeholder": "Your Number"}
            ),
            "message": widgets.TextInput(
                attrs={"class": "required form-control", "placeholder": "Your message"}
            ),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "phone","email", "subject", "message"]
        widgets = {
            "name": widgets.TextInput(
                attrs={"class": " form-control", "placeholder": "Your Name"}
            ),
            "phone": widgets.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Number"}
            ),
            "email": widgets.EmailInput(
                attrs={"class": "form-control", "placeholder": "Your Email"}
            ),
            "subject": widgets.TextInput(
                attrs={"class": "form-control", "placeholder": "Your subject"}
            ),
            "message": widgets.Textarea(
                attrs={"class": "form-control", "placeholder": "Your message", "rows": 4}
            ),
        }


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["service", "name", "message"]
        widgets = {
            "name": widgets.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Name"}
            ),
            "service": widgets.Select(
                attrs={"class": "form-control service-select", "placeholder": "Select Service"}
            ),
            "message": widgets.Textarea(
                attrs={"class": "form-control", "placeholder": "Your message"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        self.fields["service"].queryset = Product.objects.filter(is_active=True)
        self.fields["service"].empty_label = "Select Service"
