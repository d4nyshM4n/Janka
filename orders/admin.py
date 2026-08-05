from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "fullname",
        "phone",
        "total_price",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "fullname",
    )