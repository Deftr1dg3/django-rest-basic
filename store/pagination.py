from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class ProductPagination(PageNumberPagination):
    # For Limit Offset
    # default_limit = 3
    page_size = 10