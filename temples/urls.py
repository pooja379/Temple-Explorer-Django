from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("explore/", views.explore, name="explore"),

    path(
    "temple/<int:temple_id>/",
    views.temple,
    name="temple"
),

    path("favorites/", views.favorites, name="favorites"),

    path("add-temple/", views.add_temple, name="add_temple"),

    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),

    # ========= REST API =========
    path("api/temples/", views.temple_list_api, name="temple_api"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
    "favorite/<int:temple_id>/",
    views.add_favorite,
    name="add_favorite"
),
]