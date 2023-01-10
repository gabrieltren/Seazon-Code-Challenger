from rest_framework import pagination
from rest_framework.response import Response

class GeneralizedPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data, *args, **kwargs):
        return Response(
            {   
                "count":self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "totalPages": self.page.paginator.num_pages,
                "totalResults":len(data),
                "results":data,
            }
        )