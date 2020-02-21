from rest_framework import viewsets
from .models import TestModel
from .serializers import TestSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = TestModel.objects.all()
    serializer_class = TestSerializer
    filterset_fields = ['name', 'submodel', 'submodel__name']



