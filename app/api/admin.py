from app.api.models import Song
from django.contrib import admin


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_filter = ("artist", "album", "private", "favorite", "created_by")
    search_fields = [
        "name",
        "artist",
        "album",
        "created_by.username",
        "created_by.email",
    ]
    list_display = (
        "pk",
        "name",
        "artist",
        "album",
        "duration",
        "favorite",
        "private",
        "created_by",
        "created",
        "modified",
    )
