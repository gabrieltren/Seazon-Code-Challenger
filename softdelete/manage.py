from django.db.models import QuerySet, Manager
from django.utils import timezone

class SoftDeleteQuerySet(QuerySet):
    def delete(self):
        for obj in self:
            obj.deletado_em = timezone.now()
            obj.save()
            
class SoftDeleteManager(Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            deletado_em__isnull=True
        )
            