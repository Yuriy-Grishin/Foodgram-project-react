from django.contrib import admin

from users.models import User, Subscriptions


admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk',
        'username', 'email', 'password', 'first_name', 'last_name',
    )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = '-нет данных-'


admin.site.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    empty_value_display = '-нет данных-'