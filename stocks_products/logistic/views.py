from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend


class StockPagination(PageNumberPagination):
    page_size = 10  # Укажите количество элементов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ['name', 'description']  # Добавляем фильтрацию по полям
    search_fields = ['name', 'description']  # Добавляем поиск по имени и описанию


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    pagination_class = StockPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ['name', 'price', 'category']
    search_fields = ['name', 'category']