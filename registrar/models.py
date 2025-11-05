from django.db import models

class Folder(models.Model):
    folder_name = models.CharField(max_length=100)
    floor_number = models.IntegerField()
    max_size = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.folder_name

    class Meta:
        app_label = 'registrar'
