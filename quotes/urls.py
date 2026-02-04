from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.quote, name="quote"),              # / (when included at root)
    path("quote", views.quote, name="quote_page"),    # /quote
    path("show_all", views.show_all, name="show_all"),# /show_all
    path("about", views.about, name="about"),         # /about
]
