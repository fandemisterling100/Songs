from app.users.models import User
from django.db import models


class TimeStampedModel(models.Model):
    """
    Behavior to add date creted and date modified
    """

    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    modified = models.DateTimeField(auto_now=True, verbose_name="Modified")

    class Meta:
        abstract = True


class Song(TimeStampedModel):

    name = models.CharField(
        max_length=255,
        verbose_name="Name",
    )
    artist = models.CharField(
        max_length=255,
        verbose_name="Artist",
    )
    album = models.CharField(
        max_length=255,
        verbose_name="Album",
    )
    duration = models.DurationField(verbose_name="Duration")
    favorite = models.BooleanField(verbose_name="Favorite", default=False, blank=True)
    private = models.BooleanField(verbose_name="Private", default=True, blank=True)
    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Song"
        verbose_name_plural = "Songs"

    def __str__(self):
        return "{}: {} - {}".format(self.pk, self.name, self.artist)
