from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    path("school/", School, name="school"),
    path("confirm/", confirm, name="confirm"),
    path("updateprofile/<int:id>", school_update, name="updateprofile"),
    # path("schoolprofile/<int:id>", school_profile, name="schoolprofile"),
    # # headteacher
    # path(
    #     "updateheadteacher/<int:headteacher_id>",
    #     edit_headteacher,
    #     name="edit_headteacher",
    # ),
    # path("headteacher", headTeacher, name="headteacher"),
    # # offcials
    path("officials/", School_officials, name="sofficials"),
    path("addofficial/", School_official, name="addofficial"),
    path("editofficial/<int:pk>", edit_official, name="editofficial"),
    # # athletes # athlete
    # path("athletes", athletes, name="athletes"),
    # path("athlete/<int:id>", AthleteDetail, name="athlete"),
    # path("addathlete", newAthlete, name="addathlete"),
    # # ... your other URL patterns ...
    # path("importathletes/", school_import_view, name="importathletes"),
    # # team
    # path("newteam/", create_team, name="newteam"),
    # path("updateteam/<int:id>", update_team, name="updateteam"),
    # path("teams/", teamlist, name="teams"),
    # path("team/<int:id>", team_details, name="team"),
    # path("deleteteam/<int:id>", delete_team, name="deleteteam"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
