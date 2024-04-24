from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from champs.views import *


urlpatterns = [
    path("newchamp/", newChampionship, name="newchamp"),
    path("championships/", Championships, name="champs"),
    path("champ/<int:id>", Championshipdetail, name="champ"),
    path("editchamp/<int:id>", editChampionship, name="editchamp"),
    path("deletechamp/<int:id>", DeleteChampionship, name="deletechamp"),
    # season
    path("season/<int:id>", SeasonDetail, name="season"),
    path("editseason/<int:id>", EditSeason, name="editseason"),
    path("disciplines/>", disciplines, name="disciplines"),
    path("newseason/>", newSeason, name="newseason"),
    path("deleteseason/<int:id>", DeleteSeason, name="deleteseason"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
