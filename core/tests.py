from rest_framework import status
from rest_framework.test import APITestCase
import uuid
from random import randint
from .models import Imovel, Anuncio, Reserva
from core.serializers.imovel_serializers import (
    ImovelListSerializer,
    ImovelRetriveSerializer,
)


class TestImovel(APITestCase):
    url = '/api/v1/imoveis/'



    def test_get_imoveis_list(self):
        response = self.client.get(self.url)
        
        result_data = [
            ImovelListSerializer(imovel).data 
            for imovel in Imovel.objects.filter(ativo=True).order_by("-criado_em")
            ]
        if len(result_data) > 25:
            result_data = result_data[:25]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["results"], result_data)
    
    def test_get_imoveis_retrive(self):
        instance = Imovel.objects.filter(ativo=True).order_by("?").first()
        if not instance:
            instance = Imovel.objects.create()
            instance.save()
        result_data = ImovelRetriveSerializer(instance).data
        response = self.client.get(f"{self.url}{instance.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data, result_data)

    def test_post_imoveis_create(self):
        data = {
            "codigo":str(uuid.uuid4()),
            "limite_hospede":randint(0, 10),
            "qtde_banheiro":randint(1, 5),
            "animais": True if  randint(0, 1) else False,
            "valor_limpeza":randint(30, 150),
            "endereco": f"Casa {randint(1001, 9999)}",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)

    def test_delete_imoveis_destroy(self):
        data = {
            "codigo":str(uuid.uuid4()),
            "limite_hospede":randint(0, 10),
            "qtde_banheiro":randint(1, 5),
            "animais": True if  randint(0, 1) else False,
            "valor_limpeza":randint(30, 150),
            "endereco": f"Casa {randint(1001, 9999)}",
        }
        instance = Imovel.objects.create(**data)
        instance.save()
        response = self.client.delete(f"{self.url}{instance.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_new = self.client.delete(f"{self.url}{instance.id}/")
        Imovel.all_objects.filter(id=instance.id).first().super_delete()

        result_data = {"erro": "Registro não encontrado"}

        self.assertEqual(response_new.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response_new.data, dict)
        self.assertEquals(response_new.json(), result_data)

class TestReserva(APITestCase):
    url = '/api/v1/reservas/'

    def test_post_reservas_error(self):
        data_imovel = {
            "codigo":str(uuid.uuid4()),
            "limite_hospede":2,
            "qtde_banheiro":1,
            "animais": True ,
            "valor_limpeza":randint(30, 150),
            "endereco": f"Casa {randint(1001, 9999)}",
        }
        imovel = Imovel.objects.create(**data_imovel)
        imovel.save()
        anuncio = Anuncio.objects.create(imovel=imovel,nome_plataforma="AirB", taxa_plataforma=3.12)
        anuncio.save()
        data = {
            "check_in": "10/01/2023 22:24:15",
            "check_out": "09/01/2023 22:24:15",
            "preco": 400.00,
            "comentario": "acho que sim",
            "num_hospedes": 4,
            "anuncio": anuncio.id
        }

        result_data={
            "check_out": {
                "message": f"A data de check_out:'{data['check_out']}' deve ser posterior a data de check_in:'{data['check_in']}'",
                "code": "invalid"
            },
            "num_hospedes": {
                "message": f"O número máximo de hospedes é: {imovel.limite_hospede}",
                "code": "invalid"
            }
        }
        response = self.client.post(self.url, data=data)

        data = {
            "check_in": "10/01/2023 22:24:15",
            "check_out": "09/01/2023 22:24:15",
            "preco": 400.00,
            "comentario": "acho que sim",
            "num_hospedes": 2,
            "anuncio": anuncio.id
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertEquals(response.json(), result_data)

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
    