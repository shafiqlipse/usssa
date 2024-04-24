from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("newcompetition/", create_competition, name="newvcomp"),
    path("updatecompetition/<int:id>", update_competition, name="updatevcompetition"),
    path("competition/<int:id>", competition_details, name="vcompetition"),
    path("deletecompetition/<int:id>", delete_competition, name="deletevcompetition"),
    path("competitions/", competitions, name="vcomps"),
    # sports
    path(
        "generate_vfixtures/<int:vseason_id>/",
        generate_vfixtures_view,
        name="generate_vfixtures",
    ),
    path("create_season/", SeasonCreateView.as_view(), name="create_vseason"),
    path("season/<int:id>", vseason_details, name="vseason"),
    path("editfixture/<int:id>", edit_fixtures_view,name="editvfixture"),
    path("fixture/<int:id>", FixtureDetail,name="vfixture")
    # path("sportdetail/<int:id>", sport_details, name="sport_details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
