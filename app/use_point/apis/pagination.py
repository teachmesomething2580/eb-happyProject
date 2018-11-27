from rest_framework.pagination import PageNumberPagination


class UsePointResultSetPagination(PageNumberPagination):
    page_size = 51
    page_size_query_param = 'page_size'