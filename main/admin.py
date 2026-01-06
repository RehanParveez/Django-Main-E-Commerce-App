from django.contrib import admin
from main.models import ContactUs

# Register your models here.
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = 'name', 'email', 'subject', 'message'
