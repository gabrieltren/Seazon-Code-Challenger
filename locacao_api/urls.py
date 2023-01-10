"""locacao_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.urls import urlpatterns as api_core


admin.site.site_header = "API Locação"
admin.site.index_title = "Locação"
admin.site.site_title = "Painel de administração"

schema_view = get_schema_view(
    openapi.Info(
        title="API Locação",
        default_version="v1",
        description="Core API that serves models to frontend app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="gabriel.silveira1207@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

url_api = [*api_core]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('api/v1/',include(url_api)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
