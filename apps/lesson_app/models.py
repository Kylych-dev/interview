from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self) -> str:
        return f'{self.name} ---> {self.owner}'

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    video_link = models.URLField()
    duration_seconds = models.IntegerField()
    products = models.ManyToManyField(Product)
    
    def __str__(self) -> str:
        return f'{self.name} ---> {self.products}'

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_time_seconds = models.IntegerField()
    STATUS_CHOICES = (
        ('viewed', 'Просмотрено'),
        ('not_viewed', 'Не просмотрено')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='not_viewed')
    
 


