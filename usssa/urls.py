from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts.views import (
    school_registration,
    user_login,
    get_zones,
    get_districts,
    user_logout,
    dashboard,
    custom_404,
)

# from client.views import home, football
from athletes.views import calculate_age_choices

# from client.views import schools, all_schools, all_athletes, school_officials, all_teams
from school.views import school_dashboard
from client.views import home

#
from athletes.views import get_athletes, get_officials

handler404 = custom_404

# from competition.views import get_teams


urlpatterns = [
    path("admin/", admin.site.urls),
    path("school_dashboard/", school_dashboard, name="schooldash"),
    path("dashboard/", dashboard, name="dashboard"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    # path("password/", passwordReset, name="password"),
    path("register/", school_registration, name="register"),
    path("", home, name="home"),
    path("usssa/", include("client.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("champs/", include("champs.urls")),
    # path('accounts/', include('allauth.urls')),
    # zones
    path("get_zones/", get_zones, name="get_zones"),
    path("get_districts/", get_districts, name="get_districts"),
    path("calculate_age_choices/", calculate_age_choices, name="calculate_age_choices"),
    path("get_athletes/", get_athletes, name="get_athletes"),
    path("get_officials/", get_officials, name="get_officials"),
    # path("get_competitions/", get_competitions, name="get_competitions"),
    # path("get_teams/", get_teams, name="get_teams"),
    # path("get_cteams/", get_cteams, name="get_cteams"),
    # includes
    # path("accounts/", include("accounts.urls")),
    path("school/", include("school.urls")),
    path("athletes/", include("athletes.urls")),
    path("football/", include("football.urls")),
    path("basketball3/", include("basketball3.urls")),
    # path("competitions/", include("competitions.urls")),
    # path("football/", include("season.urls")),
    # path("fixtures/", include("fixtures.urls")),
    path("transfers/", include("transfers.urls")),
    path("officials/", include("officials.urls")),
    # path("venues/", include("venues.urls")),
    # path("news/", include("news.urls")),
    # # # views from urls or urls from home views
    # # path("dashboard/", schools, name="dashboard"),
    # path("schools/", all_schools, name="schools"),
    # path("athletes/", all_athletes, name="athletes"),
    # path("teams/", all_teams, name="teams"),
    # path("school_officials/", school_officials, name="school_officials"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
