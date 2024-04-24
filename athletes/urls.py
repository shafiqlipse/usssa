from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [

    # # athletes # athlete
    path("athletes", athletes, name="athletes"),
    path("athlete/<int:id>", AthleteDetail, name="athlete"),
    path("updateathlete/<int:id>", AthleteUpdate.as_view(), name="updateathlete"),
    path("addathlete", newAthlete, name="addathlete"),
    path("registration/", registration, name="registration"),
    # # ... your other URL patterns ...
    # path("importathletes/", school_import_view, name="importathletes"),
    # # team
    path("newteam/", create_team, name="newteam"),
    path("updateteam/<int:id>", update_team, name="updateteam"),
    path("teams/", teamlist, name="teams"),
    # path("team/<int:id>", team_details, name="team"),
    path("deleteteam/<int:id>", delete_team, name="deleteteam"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
