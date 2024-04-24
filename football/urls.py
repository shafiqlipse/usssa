from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("", Football, name="football"),
    path("comp/<int:id>", competition_details, name="comp"),
    path("event/<int:id>", FixtureEvent, name="fixture-event"),

    # sports
    path(
        "generate_fixtures/<int:competition_id>/",
        generate_fixtures_view,
        name="generate_fixtures",
    ),
    # path("sportdetail/<int:id>", sport_details, name="sport_details"),
    path("fixture_details/<int:id>", FixtureDetail, name="fixture"),
    path("fixture_update/<int:id>", edit_fixtures_view, name="edit_fixture"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
