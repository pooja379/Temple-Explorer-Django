from django.db import models
from django.contrib.auth.models import User

class Temple(models.Model):

    name = models.CharField(max_length=200)

    city = models.CharField(max_length=100)

    deity = models.CharField(max_length=100)

    famous_for = models.TextField(blank=True)

    history = models.TextField(blank=True)

    timings = models.TextField(blank=True)

    festivals = models.TextField(blank=True)

    architecture = models.TextField(blank=True)

    facts = models.TextField(blank=True)

    latitude = models.FloatField()

    longitude = models.FloatField()

    image_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name
class Review(models.Model):

    temple = models.ForeignKey(
        Temple,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    username = models.CharField(max_length=100)

    rating = models.IntegerField()

    review = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.temple.name}"


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    temple = models.ForeignKey(
        Temple,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "temple")