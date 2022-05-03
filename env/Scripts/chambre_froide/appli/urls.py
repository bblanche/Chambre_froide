from .views import index, liste
from django.urls import path

app_name = 'appli'
urlpatterns = [
    path('', index , name="index"),
    path('/details', liste , name="liste"),
]