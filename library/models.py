from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150, null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField("ISBN", max_length=20, unique=True, null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)

    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'library'

