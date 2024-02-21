from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .yasg import urlpatterns as doc_ts
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.v1.route")),
    path("", include("apps.pages.urls", namespace="pages")),
]
urlpatterns += doc_ts

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
        modified:   api/auth/serializers.py
        modified:   api/v1/route.py
        modified:   apps/accounts/models.py

'''
