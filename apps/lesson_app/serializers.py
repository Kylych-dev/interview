from rest_framework import serializers
from .models import Product, Lesson, LessonProgress

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'owner')

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'video_link', 'duration_seconds', 'products')

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ('id', 'user', 'lesson', 'viewed_time_seconds', 'status')
