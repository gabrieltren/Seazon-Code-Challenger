from rest_framework import routers

from .views.anuncio import AnuncioViewSet
from .views.imovel import ImovelViewSet
from .views.reserva import ReservaViewSet

router = routers.DefaultRouter()

router.register("anuncios", AnuncioViewSet, basename="anuncios")
router.register("imoveis", ImovelViewSet, basename="imoveis")
router.register("reservas", ReservaViewSet, basename="reservas")


urlpatterns = router.urls