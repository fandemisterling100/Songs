from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class SongsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "results": data,
                "meta": {
                    "page_count": self.page.paginator.num_pages,
                    "total_results": self.page.paginator.count,
                    "current_page_no": self.page.number,
                    "limit": self.page_size,
                    "last_page": self.page.has_next(),
                },
            },
            status=status.HTTP_200_OK,
        )