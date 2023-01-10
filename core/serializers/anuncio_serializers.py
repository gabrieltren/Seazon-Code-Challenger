from django.conf import settings
from rest_framework import serializers
import pytz

from core.models import Imovel, Anuncio, Reserva


class AnuncioListSerializer(serializers.ModelSerializer):

    imovel = serializers.SerializerMethodField()

    def get_imovel(self, obj):
        return Imovel.objects.filter(id=obj.imovel.id).values(
            "id","codigo","limite_hospede","qtde_banheiro",
            "animais", "valor_limpeza", "endereco"
        ).first()

    def get_reservas(self, obj):
        return Reserva.objects.filter(anucio=obj).count()

    class Meta:
        model = Anuncio
        fields = "__all__"


class AnuncioRetriveSerializer(serializers.ModelSerializer):
    
    imovel = serializers.SerializerMethodField()
    reservas = serializers.SerializerMethodField()


    def get_imovel(self, obj):
        return Imovel.objects.filter(id=obj.imovel.id).values(
            "id","codigo","limite_hospede","qtde_banheiro",
            "animais", "valor_limpeza", "endereco"
        ).first()

    def get_reservas(self, obj):
        return Reserva.objects.filter(anucio=obj).count()

    class Meta:
        model = Anuncio
        fields = "__all__"


class AnuncioCreateSerializer(serializers.ModelSerializer):
    taxa_plataforma = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        model = Anuncio
        fields = [
            "imovel",
            "nome_plataforma",
            "taxa_plataforma",
            "ativo",
        ]

class AnuncioUpdateSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Anuncio
        fields = [
            "imovel",
            "nome_plataforma",
            "taxa_plataforma",
            "ativo",
        ]