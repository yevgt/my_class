from rest_framework.pagination import CursorPagination

# пагинация
class CustomCursorPagination(CursorPagination):
    page_size = 6
    ordering = 'created_at'