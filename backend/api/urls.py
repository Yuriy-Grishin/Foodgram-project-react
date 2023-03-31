from djoser.views import TokenCreateView, TokenDestroyView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CreateUserView,
    UsersListViewSet,
    ProductViewSet,
    RecipeViewSet,
    TagViewSet,
)

"""Регистрируем роутеры, используем DefaultRouter чтобы вернуть список всех ресурсов api"""
"""basename не указывается, формируется автоматически из названия моделей т.к. есть queryset во viewset"""
router = DefaultRouter()
router.register("users", UsersListViewSet)
router.register("products", ProductViewSet)
router.register("recipes", RecipeViewSet)
router.register("tags", TagViewSet)


"""Добавояем аутентификацию по токену для тестирования в Postman. Включаем все зарегистрированные роутеры в urlpatterns чтобы они были доступны"""
urlpatterns = [
    path("auth/token/login/", TokenCreateView.as_view(), name="login"),
    path("auth/token/logout/", TokenDestroyView.as_view(), name="logout"),
    path("auth/", include("djoser.urls.authtoken")),
    path("users/create/", CreateUserView.as_view(), name="userscreate"),
    path("", include(router.urls)),
]
