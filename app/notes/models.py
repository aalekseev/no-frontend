from django.db import models

from accounts.models import CustomUser


class Note(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("notes:update", kwargs={"pk": self.pk})
