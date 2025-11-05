from django.db import models

class StudentFolder(models.Model):
    id = models.AutoField(primary_key=True)
    folder_name = models.CharField(max_length=255)
    folder_id = models.CharField(max_length=100, unique=True)
    lname = models.CharField("Last Name", max_length=100)
    fname = models.CharField("First Name", max_length=100)
    midname = models.CharField("Middle Name", max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=255, editable=False)

    class Meta:
        app_label = 'registrar'
        db_table = 'student_folders'
        ordering = ['lname', 'fname']

    def __str__(self):
        return f"{self.full_name} ({self.folder_id})"

    def save(self, *args, **kwargs):
        # Automatically build full_name before saving
        middle = f" {self.midname}" if self.midname else ""
        self.full_name = f"{self.fname}{middle} {self.lname}"
        super().save(*args, **kwargs)
