from django.urls import path
from .views import athlete_list, transfer_athlete

urlpatterns = [
    path('athletes/', athlete_list, name='tathlete_list'),
    path('initiate_transfer/<int:id>/', transfer_athlete, name='initiate_transfer'),
]
