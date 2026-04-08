from django.db import models

class Dictionary(models.Model):
    word = models.CharField(max_length=255, unique=True)
    definition = models.TextField(blank=True, null=True)  # Izoh uchun maydon

    def __str__(self):
        return self.word