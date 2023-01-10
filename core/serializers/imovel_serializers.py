from django.conf import settings
from rest_framework import serializers
import pytz

from core.models import Imovel, Anuncio


class ImovelListSerializer(serializers.ModelSerializer):


    class Meta:
        model = Imovel
        fields = "__all__"


class ImovelRetriveSerializer(serializers.ModelSerializer):
    
    anuncios = serializers.SerializerMethodField()

    def get_anuncios(self, obj):
        return Anuncio.objects.filter(imovel=obj).count()

    class Meta:
        model = Imovel
        fields = "__all__"


class ImovelCreateSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Imovel
        fields = [
            "codigo",
            "limite_hospede",
            "qtde_banheiro",
            "animais",
            "valor_limpeza",
            "endereco",
            "ativo",
        ]

class ImovelUpdateSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Imovel
        fields = [
            "codigo",
            "limite_hospede",
            "qtde_banheiro",
            "animais",
            "valor_limpeza",
            "endereco",
            "ativo",
        ]