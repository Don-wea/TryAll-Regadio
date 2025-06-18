from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('riego_api.urls')),
    path('test/', include('mongo_models.urls')),
    # path('my_maps/', include('my_maps.urls')),
]
