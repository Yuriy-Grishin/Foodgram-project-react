from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from recipes.views import shopping_cart

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("api/", include("api.urls", namespace="api")),
    path("staff/", include([
        path("shopping_cart/<int:pk>/", shopping_cart, name='shopping_cart')
    ]))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
