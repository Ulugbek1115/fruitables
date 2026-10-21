from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings          # <--- Добавьте эту строчку
from django.conf.urls.static import static # <--- И эту строчку

from main import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('contact/', views.contact, name='contact'),
)

# --- Добавьте этот блок в самый конец файла ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)