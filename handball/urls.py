from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("newcompetition/", create_competition, name="newhcomp"),
    path("updatecompetition/<int:id>", update_competition, name="updatehcompetition"),
    path("competition/<int:id>", competition_details, name="hcompetition"),
    path("deletecompetition/<int:id>", delete_competition, name="deletehcompetition"),
    path("competitions/", competitions, name="hcomps"),
    # sports
    path(
        "generate_hfixtures/<int:hseason_id>/",
        generate_hfixtures_view,
        name="generate_hfixtures",
    ),
    path("create_season/", HSeasonCreateView.as_view(), name="create_hseason"),
    path("season/<int:id>", season_details, name="hseason"),
    path("editfixture/<int:id>", edit_hfixtures_view, name="edithfixture"),
    path("fixture/<int:id>", FixtureDetail, name="hfixture")
    # path("sportdetail/<int:id>", sport_details, name="sport_details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
