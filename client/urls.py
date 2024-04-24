from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from football.futviews import *

from .views import *


# from .basketviews import *


urlpatterns = [
    # about pages
    path("about/", about, name="about"),
    path("events/", events, name="events"),
    path("contact/", contact, name="contact"),
    path("championship/<int:id>", championship, name="champd"),
    # path("football_teams/", footballTeams, name="football_teams"),
    path("football_fixtures/", footballFixtures, name="football_fixtures"),
    # path("football_stats/<int:id>", footballStatistics, name="footballstatistics"),
    path("football_results/", footballResults, name="football_results"),
    path("football_standings/", footballStandings, name="football_standings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
