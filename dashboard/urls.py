from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    path("school/", School, name="school"),
    path("school/<int:id>", school_detail, name="dschool"),

    path("schools/", schools, name="schools"),
    path("athletes/", all_athletes, name="aathletes"),
    path("officials/", all_officials, name="aofficials"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
