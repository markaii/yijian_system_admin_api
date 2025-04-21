import math
from collections import OrderedDict

from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class  PageNumberPaginationEx(PageNumberPagination):
    page_size_query_param = 'size'
    # page_size = 10
    # max_page_size = 1000
    """
     /**
     * total : 1
     * size : 10
     * pages : 1
     * current : 1
     * records : [{"id":20,"delFlag":"0","createBy":17,"createTime":"2018-09-14 03:28:49","updateBy":null,"updateTime":null,"ids":null,"managerId":17,"name":"kam联盟","code":"100013","province":440000,"city":440100,"district":440113,"address":"华南理工大学图书馆(广州市番禺区)","longitude":113.4057096,"latitude":23.0472244,"shopType":"5","contact":"kam","logo":null,"tel":"123","star":5,"intro":null}]
     */
    """
    total = 0

    def paginate_queryset(self, queryset, request, view=None):
        # self.total = self._get_count(queryset)
        self.total = queryset.count()
        self.page_size = self.get_page_size(request)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return OrderedDict([
            ('total', self.total),  # 总记录数
            # ('size', self.page_size),  # 单页数量
            ('size', len(self.page)),  # 单页数量
            ('pages', math.ceil(self.total / self.page_size)),  # 总分页数
            ('current', self.page.number),  # 当前页码
            ('records', data)
        ])
