'''  ШАБЛОНЫ URL '''
''' Конфигурация URL-адресов для административной панели в соответствии c URL-адресами из модуля elibrary_app.urls '''

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('elibrary_app.urls'))
]

if settings.DEBUG or not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)