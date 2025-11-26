from django.db import models

# Create your models here.

class details(models.Model):
    name=models.CharField(max_length=100)
    roll_no=models.PositiveIntegerField(unique=True)

class resume(models.Model):
    resume_file=models.FileField(upload_to='resumes/',blank=True,null=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.subject})"
