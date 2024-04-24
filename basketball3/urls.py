from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("basketball3/", basketball3, name="basketball3"),
 
    # sports
    path(
        "generate_b3fixtures/<int:b3season_id>/",
        generate_b3fixtures_view,
        name="generate_b3fixtures",
    ),

    path("editfixture/<int:id>", edit_b3fixtures_view, name="editb3fixture"),
    path("fixture/<int:id>", FixtureDetail, name="b3fixture")
    # path("sportdetail/<int:id>", sport_details, name="sport_details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
