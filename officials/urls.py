from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    # venues

    path("newofficial/", create_official, name="newofficial"),
    path("updateofficial/<int:id>", update_official, name="updateofficial"),
    path("official/<int:id>", official_details, name="official"),
    path("deleteofficial/<int:id>", delete_official, name="deleteofficial"),
    path("officials/", officials, name="officials"),
    # competition
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
