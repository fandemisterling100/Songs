from rest_framework_simplejwt.views import TokenRefreshView

from app.api import views
from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("register", views.UserRegisterApiView.as_view(), name="register"),
    # JWT authentication
    path("public/token", views.UserLoginView.as_view(), name="token_obtain_pair"),
    path("public/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    # Songs API
    path(
        "songs/create",
        views.SongCreateAPIView.as_view(),
        name="create_song",
    ),
    path(
        "songs/<int:pk>/update",
        views.SongUpdateAPIView.as_view(),
        name="update_song",
    ),
    path(
        "songs/<int:pk>/delete",
        views.SongDeleteApiView.as_view(),
        name="delete_song",
    ),
    path(
        "songs/<int:pk>/",
        views.SongRetrieveAPIView.as_view(),
        name="retrieve_song",
    ),
    path(
        "songs/public",
        views.PublicSongsListAPIView.as_view(),
        name="retrieve_all_public_songs",
    ),
    path(
        "songs",
        views.SongListAPIView.as_view(),
        name="retrieve_all_songs",
    ),
    path(
        "random-number",
        views.GenerateRandomNumberAPIView.as_view(),
        name="random_number",
    ),
]
