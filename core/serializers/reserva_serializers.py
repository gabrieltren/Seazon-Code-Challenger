from django.conf import settings
from rest_framework import serializers
import pytz
from datetime import datetime
from core.models import Imovel, Anuncio, Reserva



class ReservaListSerializer(serializers.ModelSerializer):
    check_in = serializers.DateTimeField(
        format=settings.DATE_TIME_OUTPUT
        )
    check_out = serializers.DateTimeField(
        format=settings.DATE_TIME_OUTPUT
        )
    anuncio = serializers.SerializerMethodField()

    def get_anuncio(self, obj):
        return Anuncio.objects.filter(id=obj.anuncio.id).values(
            "id","nome_plataforma", "taxa_plataforma",
        ).first()


    class Meta:
        model = Reserva
        fields = "__all__"


class ReservaRetriveSerializer(serializers.ModelSerializer):
    check_in = serializers.DateTimeField(
        format=settings.DATE_TIME_OUTPUT
        )
    check_out = serializers.DateTimeField(
        format=settings.DATE_TIME_OUTPUT
        )
    imovel = serializers.SerializerMethodField()
    anuncio = serializers.SerializerMethodField()


    def get_imovel(self, obj):
        return Imovel.objects.filter(id=obj.anuncio.imovel.id).values(
            "id", "codigo","limite_hospede","qtde_banheiro",
            "animais", "valor_limpeza", "endereco"
        ).first()

    def get_anuncio(self, obj):
        return Anuncio.objects.filter(id=obj.anuncio.id).values(
            "id", "nome_plataforma", "taxa_plataforma",
        ).first()

    class Meta:
        model = Reserva
        fields = "__all__"


class ReservaCreateSerializer(serializers.ModelSerializer):
    check_in = serializers.DateTimeField(
        input_formats=settings.DATE_TIME_INPUT,
        format=settings.DATE_TIME_OUTPUT,
        required=False,
        allow_null = True
        )
    check_out = serializers.DateTimeField(
        input_formats=settings.DATE_TIME_INPUT,
        format=settings.DATE_TIME_OUTPUT,
        required=False,
        allow_null = True
        )
    
    class Meta:
        model = Reserva
        fields = [
            "anuncio",
            "check_in",
            "check_out",
            "preco",
            "comentario",
            "num_hospedes",
            "ativo",
        ]

    def _validade_check_in__check_out(self):
        check_in = self.initial_data["check_in"] if "check_in" in self.initial_data else None
        check_out = self.initial_data["check_out"] if "check_out" in self.initial_data else None
        if check_in and check_out:
            
            if datetime.strptime(check_in, "%d/%m/%Y %H:%M:%S") >= datetime.strptime(check_out, "%d/%m/%Y %H:%M:%S"):
                raise serializers.ValidationError({
                    "check_out": "A data de check_out:'{check_out}' deve ser posterior a data de check_in:'{check_in}'"
                })
        return None
    def _validate_total_hospede(self):
        hospedes = self.initial_data["num_hospedes"] if "num_hospedes" in self.initial_data else None
        if hospedes:
            imovel = Imovel.objects.filter(
                id=Anuncio.objects.filter(id=self.initial_data["anuncio"]).first().imovel.id,
                ativo=True
                ).first()
            if not imovel:
                raise serializers.ValidationError({
                    "anuncio": "Imóvel do anúncio não está disponível"
                })
            if hospedes > imovel.limite_hospede:
                raise serializers.ValidationError({
                    "num_hospedes": f"O número máximo de hospedes é: {imovel.limite_hospede}"
                })
        return None

    def validate(self, *args, **kwargs):
        dict_erro = dict()
        
        try:
            self._validade_check_in__check_out()
        except serializers.ValidationError as exc:
            dict_erro.update(**exc.get_full_details())
        
        try:
            self._validate_total_hospede()
        except serializers.ValidationError as exc:
            dict_erro.update(**exc.get_full_details())

        
        if dict_erro:
            raise serializers.ValidationError(dict_erro)

        return super().validate(*args, **kwargs)

class ReservaUpdateSerializer(serializers.ModelSerializer):
    check_in = serializers.DateTimeField(
        format=settings.DATE_TIME_OUTPUT, 
        input_formats=settings.DATE_TIME_INPUT,
        allow_null = True
        )
    check_out = serializers.DateTimeField(
        format=settings.DATE_TIME_OUTPUT,
        input_formats=settings.DATE_TIME_INPUT,
        required=False,
        allow_null = True
        )


    class Meta:
        model = Reserva
        fields = [
            "codigo",
            "anuncio",
            "check_in",
            "check_out",
            "preco",
            "comentario",
            "num_hospedes",
            "ativo",
        ]