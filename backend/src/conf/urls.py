from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, \
    SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/storage/', include('storage.urls')),
    path('api/telegram/mini_app/', include('telegram_mini_app.urls')),
    path('api/telegram/bot/', include('telegram_bot.urls')),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
