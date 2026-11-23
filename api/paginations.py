from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 2  # Number of items per page
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 1  # Maximum items per page

    def get_paginated_response(self, data):
        return Response({
            
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.page_size,
            'count': self.page.paginator.count,
            'results': data
        })