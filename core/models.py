from django.db import models
import uuid
from django.utils import timezone
from softdelete.models import SoftDeleteModel



class Imovel(SoftDeleteModel):
    
    codigo = models.CharField(
        "Codigo do Imóvel", 
        max_length=128, blank=True, 
        null=True, default=uuid.uuid4,
        unique=True
        )
    limite_hospede = models.IntegerField("Limite de Hóspedes", default=0)
    qtde_banheiro = models.IntegerField("Quantide de Banheiros", default=0)
    animais = models.BooleanField(default=False)
    valor_limpeza = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    endereco = models.CharField(
        "Endereço do Imóvel", 
        max_length=256, blank=True, 
        null=True,
        )

    class Meta:
        verbose_name = "Imóvel"
        verbose_name_plural = "Imóveis"
    
    def __str__(self) -> str:
        return f"{self.codigo}"

    def delete(self, *args, **kwargs):
        self.deletado_em = timezone.now()
        self.save()
        Anuncio.objects.filter(imovel_id=self.id).delete()

class Anuncio(SoftDeleteModel):
    imovel = models.ForeignKey(
        Imovel,
        related_name="anucio_imovel",
        on_delete=models.CASCADE,
        verbose_name='Imóvel'
    )
    nome_plataforma = models.CharField("Nome da Plataforma", max_length=128)
    taxa_plataforma = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)
    
    class Meta:
        verbose_name = "Anúcio"
        verbose_name_plural = "Anúncios"

    def __str__(self) -> str:
        return f"{self.nome_plataforma}"

    def delete(self, *args, **kwargs):
        self.deletado_em = timezone.now()
        self.save()
        Reserva.objects.filter(anuncio_id=self.id).delete()
    

class Reserva(SoftDeleteModel):
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    anuncio = models.ForeignKey(
        Anuncio,
        related_name="reserva_anucio",
        on_delete=models.CASCADE,
        verbose_name="Reserva"
    )
    check_in = models.DateTimeField(null=True, blank=True, default=None)
    check_out = models.DateTimeField(null=True, blank=True, default=None)
    preco = models.DecimalField(max_digits=15, decimal_places=2, default=0.00 )
    comentario = models.TextField(null=True, blank=True)
    num_hospedes = models.IntegerField(default=0)
    

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self) -> str:
        return f"Reservar: {self.codigo} - {self.anucio.nome_plataforma}"


    