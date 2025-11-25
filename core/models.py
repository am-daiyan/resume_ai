from django.db import models

# Create your models here.

class details(models.Model):
    name=models.CharField(max_length=100)
    roll_no=models.PositiveIntegerField(unique=True)

class resume(models.Model):
    resume_file=models.FileField(upload_to='resumes/',blank=True,null=True)