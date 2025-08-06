from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'teacher'),
        ('student', 'student'),
    )
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profile_pictures')
    bio = models.TextField()
    role = models.CharField(choices=ROLE_CHOICES, default='student',max_length=16)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Category(models.Model):
    category_name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=40, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name

class Course(models.Model):
    course_name = models.CharField(max_length=64, unique=True)
    course_image = models.ImageField(null=True, blank=True, upload_to='course_images')
    course_video = models.FileField(null=True, blank=True, upload_to='course_videos')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ManyToManyField(SubCategory)
    LEVEL_CHOICES = (
        ('beginner', 'beginner'),
        ('intermediate', 'intermediate'),
        ('advanced', 'advanced'),
    )
    level = models.CharField(choices=LEVEL_CHOICES, default='beginner', max_length=40)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    video_lesson = models.FileField(null=True, blank=True, upload_to='video_lessons')
    docs_lesson = models.FileField(null=True, blank=True, upload_to='docs_lessons')
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.course}, {self.title}'

class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    due_time = models.DateField()
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.lesson}, {self.title}'

class Certificate(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateField(auto_now_add=True)
    certificate_url = models.FileField(null=True, blank=True, upload_to='certificates')

    def __str__(self):
        return f'{self.student}, {self.course}'

class Language(models.Model):
    language_name = models.CharField(max_length=40, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.language_name