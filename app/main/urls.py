from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from main.views import HomepageView


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("accounts/", include("django.contrib.auth.urls")),
        path("", HomepageView.as_view()),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
