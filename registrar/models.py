from django.db import models


class Folder(models.Model):
    folder_name = models.CharField(max_length=100)
    floor_number = models.IntegerField()
    max_size =  models.IntegerField()

    def __str__(self):
        return self.folder_name

    class Meta:
        app_label = 'registrar'




class Program(models.Model):
    program_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True,default='No major description provided.')

    def __str__(self):
        return f"{self.program_name} {self.description}"

    class Meta:
        app_label = 'registrar'

class Curriculum(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='curriculums')    
    academic_year = models.CharField(max_length=20)
    effective_semester = models.CharField(max_length=20)
    effective_year = models.IntegerField()

    def __str__(self):
        return f"{self.program.program_name} - {self.academic_year} ({self.effective_semester} {self.effective_year})"
    
    class Meta:
        app_label = 'registrar'

class Course(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE,default=0, related_name='courses')
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=200,default='No Title')
    lab_units = models.IntegerField(default=0)
    lec_units = models.IntegerField(default=0)
    prerequisites = models.CharField(max_length=200, blank=True, null=True)
    semester_offered = models.CharField(max_length=20,default='Not Specified')
    year_level = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.course_code} - {self.course_title}"
    
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

    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name='students'
    )

    last_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128)
    

    @property
    def full_name(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name}."

    def __str__(self):
        return self.full_name

    class Meta:
        app_label = 'registrar'
       