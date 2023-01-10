
from django.db import models

from django.utils import timezone
from .manage import SoftDeleteManager

class SoftDeleteModel(models.Model):
    class Meta:
        abstract = True
        ordering = ["-created_at",]
        
    criado_em = models.DateTimeField("Criado em",auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado_em", auto_now=True)
    deletado_em = models.DateTimeField("Deletado em", null=True, blank=True)
    ativo = models.BooleanField(default=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()
        
    def delete(self, *args, **kwargs):
        self.deletado_em = timezone.now()
        self.save()
        
    def super_delete(self, *args, **kwargs):
        super(SoftDeleteModel, self).delete(*args, **kwargs)