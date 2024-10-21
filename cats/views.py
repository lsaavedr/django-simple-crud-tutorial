# cats/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cats.models import Cat
from cats.serializers import CatSerializer


class CatViewSet(ModelViewSet):
    """
    Cat ViewSet
    """

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [IsAuthenticated]
