from django.db import models
from django.contrib.auth.models import AbstractUser
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
import datetime

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

LENGTH_16 = 16
LENGTH_32 = 32
LENGTH_64 = 64
LENGTH_128 = 128
LENGTH_255 = 255


class Teacher(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    rut_without_digit = models.IntegerField(unique=True)
    rut_digit = models.CharField(
        blank=True, null=True, max_length=LENGTH_16)
    first_name = models.CharField(
        blank=True, null=True, max_length=LENGTH_128)
    paternal_name = models.CharField(
        blank=True, null=True, max_length=LENGTH_128)
    maternal_name = models.CharField(
        blank=True, null=True, max_length=LENGTH_128)
    role = models.CharField(blank=True, null=True, max_length=LENGTH_16)

    class Meta:
        ordering = ('created',)


class Course(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    institution = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created',)


class Student(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    rut_without_digit = models.IntegerField(unique=True)
    rut_digit = models.CharField(
        blank=True, null=True, max_length=LENGTH_16)
    first_name = models.CharField(
        blank=True, null=True, max_length=LENGTH_128)
    paternal_name = models.CharField(
        blank=True, null=True, max_length=LENGTH_128)
    maternal_name = models.CharField(
        blank=True, null=True, max_length=LENGTH_128)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='student_set')

    class Meta:
        ordering = ('created',)


class CourseWorker(models.Model):
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='teacher_set')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Attendance(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course_set')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_set')

    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(null=True, blank=True)
