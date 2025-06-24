from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="API Regadío",
      default_version='v1',
      description="Documentación de la API Login y Usuarios",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('riego_api.urls')),
    path('test/', include('mongo_models.urls')),
    # path('my_maps/', include('my_maps.urls')),
    path('login/', include('regadio_backend.login.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
