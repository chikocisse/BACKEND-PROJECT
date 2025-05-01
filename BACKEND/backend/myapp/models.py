from django.db import models
from django.contrib.auth.models import AbstractUser


class Submission(models.Model):
    student_name = models.CharField(max_length=255)
    submitted_file = models.FileField(upload_to='submissions/')
    grade = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.grade or 'Not graded'}"


class PlagiarismResult(models.Model):
    student_a = models.CharField(max_length=100)
    student_b = models.CharField(max_length=100)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student_a', 'student_b')

    def __str__(self):
        return f"{self.student_a} vs {self.student_b} : {self.score}"


class PlagiarismCheck(models.Model):
    file = models.FileField(upload_to='plagiarism_checks/')
    plagiarism_score = models.FloatField(null=True, blank=True)
    corrected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File: {self.file.name}, Score: {self.plagiarism_score or 'Not computed'}"


    class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    # Pour éviter les conflits avec Django Admin
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myapp_customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myapp_customuser_permissions_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

