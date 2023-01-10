from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('shopping_cart',)
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "shopping_cart"
    )
    list_filter = ("first_name", "email")

    def shopping_cart(self, obj):
        return format_html(
            '<a href="{}">Download file</a>',
            reverse('shopping_cart', args=[obj.pk, ])
        )


class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author"
    )
