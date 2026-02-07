from django.urls import path
from . import views

app_name = "restaurant"

urlpatterns = [
    path("main/", views.main, name="main_page"),    # /main
    path("order/", views.order , name="order"),# /order 
    path("confirmation/", views.confirmation, name="confirmation"),  # /confirmation 
]
