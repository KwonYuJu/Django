from django.db import models

class Movie(models.Model):
  title = models.CharField(max_length=20)
  content = models.TextField()
  image = models.ImageField(blank=True, null=True)
