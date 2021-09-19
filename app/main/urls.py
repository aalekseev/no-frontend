from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("accounts/", include("django.contrib.auth.urls")),
        path("", include("notes.urls", namespace="notes")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
