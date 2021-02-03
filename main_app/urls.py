from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

API_V1 = DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="KeepUp API",
        default_version='v1',
        description="KeepUp project API list",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include('apps.core.urls')),
    path('user/', include('apps.user.urls')),
    path('exams/', include('apps.exam.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(API_V1.urls)),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
