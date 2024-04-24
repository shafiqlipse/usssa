from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("newcompetition/", create_competition, name="newb5comp"),
    path("updatecompetition/<int:id>", update_competition, name="updateb5competition"),
    path("competition/<int:id>", competition_details, name="b5competition"),
    path("deletecompetition/<int:id>", delete_competition, name="deleteb5competition"),
    path("competitions/", competitions, name="b5comps"),
    # sports
    path(
        "generate_b5fixtures/<int:b5season_id>/",
        generate_fixtures_view,
        name="generate_b5fixtures",
    ),

    path("editfixture/<int:id>", edit_b5fixtures_view, name="editb5fixture"),
    path("fixture/<int:id>", FixtureDetail, name="b5fixture")
    # path("sportdetail/<int:id>", sport_details, name="sport_details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
