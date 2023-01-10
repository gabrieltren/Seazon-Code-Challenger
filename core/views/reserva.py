
from django.utils import timezone
from rest_framework import viewsets, mixins, filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from core.paginator import GeneralizedPagination
from core.models import Reserva
from core.serializers.reserva_serializers import (
    ReservaListSerializer,
    ReservaRetriveSerializer,
    ReservaCreateSerializer,
    ReservaUpdateSerializer,
)


class ReservaViewSet(viewsets.ModelViewSet):
    pagination_class = GeneralizedPagination
    serializer_class = ReservaListSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]

    ordering_fields = [
        "criado_em",
        "preco",
        "check_in",
        "check_out",
    ]
    ordering = ["-criado_em"]

    def get_queryset(self):
        return Reserva.objects.all().order_by('-criado_em')

    def get_serializer_class(self):
        serializer_map = {
            "list": ReservaListSerializer,
            "retrieve": ReservaRetriveSerializer,
            "create": ReservaCreateSerializer,
            "update": ReservaUpdateSerializer,
            "partial_update": ReservaUpdateSerializer,
        }
        return serializer_map.get(self.action, super().get_serializer_class())
    
    def get_paginated_response(self, data, *args, **kwargs):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()


        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                serializer.data
            )
    
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_queryset().filter(id=pk).first()

        if not instance:
            return Response(
                {"erro": "Registro não encontrado "},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(instance, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request,pk=None,*args, **kwargs):
        kwargs['partial'] = True
        return self.update(request,pk,*args, **kwargs)

    def update(self, request,pk=None,*args, **kwargs):
        partial = partial = kwargs.pop('partial', False)
        data = request.data

        instance = self.get_queryset().filter(id=pk).first()

        if not instance:
            return Response(
                {"erro": "Registro não encontrado "},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 
    
    
    def destroy(self, request,pk=None,*args, **kwargs):

        instance = self.get_queryset().filter(id=pk).first()

        if not instance:
            return Response(
                {"erro": "Registro não encontrado "},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        return Response(status=status.HTTP_200_OK)