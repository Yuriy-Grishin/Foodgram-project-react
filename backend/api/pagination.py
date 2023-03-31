from rest_framework.pagination import PageNumberPagination


class LimitPagination(PageNumberPagination):
    """Позволяет пользователю устанавливать размер страницы под каждый запрос"""

    page_size_query_param = "limit"
