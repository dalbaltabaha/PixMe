from rest_framework.pagination import CursorPagination as BaseCursorPagination


class CursorPagination(BaseCursorPagination):
    ordering = '-created_at'
