from django.db import models


class Folder(models.Model):
    folder_name = models.CharField(max_length=100)
    floor_number = models.IntegerField()
    max_size =  models.IntegerField()

    def __str__(self):
        return self.folder_name

    class Meta:
        app_label = 'registrar'


class Student(models.Model):
    # Link student to a folder
    folder = models.ForeignKey(
        Folder, 
        on_delete=models.SET_NULL,  # choose what happens when folder is deleted
        null=True, 
        blank=True,
        related_name='students'
    )


    last_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128)
    

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        app_label = 'registrar'
       