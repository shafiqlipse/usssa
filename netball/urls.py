from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("newcompetition/", Ncreate_competition, name="newncomp"),
    path("updatecompetition/<int:id>", Nupdate_competition, name="updatecompetition"),
    path("competition/<int:id>", Ncompetition_details, name="ncompetition"),
    path("deletecompetition/<int:id>", Ndelete_competition, name="deletecompetition"),
    path("ncompetitions/", Ncompetitions, name="ncomps"),
    # sports
    path(
        "generate_fixtures/<int:nseason_id>/",
        Ngenerate_fixtures_view,
        name="generate_nfixtures",
    ),
    path("create_season/", NSeasonCreateView.as_view(), name="create_nseason"),
    path("season/<int:id>", Nseason_details, name="nseason"),
    path("editfixture/<int:id>", Nedit_fixtures_view, name="editfixture"),
    path("fixture/<int:id>", NFixtureDetail, name="fixture")
    # path("sportdetail/<int:id>", sport_details, name="sport_details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
