from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("newcompetition/", create_competition, name="newcomp"),
    path("updatecompetition/<int:id>", update_competition, name="updatecompetition"),
    path("competition/<int:id>", competition_details, name="competition"),
    path("deletecompetition/<int:id>", delete_competition, name="deletecompetition"),
    path("competitions/", competitions, name="comps"),
    # sports
    path(
        "generate_fixtures/<int:season_id>/",
        generate_fixtures_view,
        name="generate_fixtures",
    ),
    path("create_season/", SeasonCreateView.as_view(), name="create_season"),
    path("season/<int:id>", season_details, name="season"),
    path("editfixture/<int:id>", edit_fixtures_view,name="editfixture"),
    path("fixture/<int:id>", FixtureDetail,name="fixture")
    # path("sportdetail/<int:id>", sport_details, name="sport_details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
