from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response

from django.http import JsonResponse

from . import models
from . import serializers


from django.core import serializers as core_serializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_lessons(request):
    print('************************************')
    user = request.user.id
    print(user, '****************************')
    products = models.Lesson.objects.filter(id=user)
    serializer = serializers.LessonSerializer(products, many=True)
    return Response(serializer.data)


# Список всех уроков по всем продуктам с информацией 
@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
def lessons_list(request):
    print('--------------------------------------')

    user = request.user.id
    lesson_progress = models.LessonProgress.objects.filter(user=user)
    print(lesson_progress)
    serializer = serializers.LessonProgressSerializer(lesson_progress, many=True)

    return Response(serializer.data)

    # print('_____')

    # print(serializer)

    # print('_____')

    # serialized_data = []
    # print('909090909090090')

    # for progress in lesson_progress:
    #     lesson = progress.lesson
    #     serialized_data.append({
    #         'lesson_id': lesson.id,
    #         'lesson_name': lesson.name,
    #         'video_link': lesson.video_link,
    #         'duration_seconds': lesson.duration_seconds,
    #         'status': progress.status,
    #         'viewed_time_seconds': progress.viewed_time_seconds
    #     })
    # serializer = serializers.LessonProgressSerializer(serialized_data, many=True)

    # return Response(serialized_data)



# Список уроков по конкретному продукту с информацией
@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
def lessons_list(request, product_id):
    user = request.user.id
    try:
        product = models.Product.objects.get(id=product_id, owner=user)
        # serializer = serializers.ProductSerializer(product)
    except models.Product.DoesNotExist:
        return Response({'detail': 'Продукт не найден или не принадлежит вам.'}, status=400)

    lessons = models.Lesson.objects.filter(products=product)
    # serializer_lesson = serializers.LessonSerializer(lessons)
    serialized_data = []  # Сюда будем добавлять данные о уроках для пользователя

    for lesson in lessons:
    # for lesson in serializer_lesson:
        try:
            progress = models.LessonProgress.objects.get(user=user, lesson=lesson)
            last_viewed_time = progress.viewed_time_seconds
        except models.LessonProgress.DoesNotExist:
            last_viewed_time = 0

        serialized_data.append({
            'lesson_id': lesson.id,
            'lesson_name': lesson.name,
            'video_link': lesson.video_link,
            'duration_seconds': lesson.duration_seconds,
            'status': progress.status if last_viewed_time >= lesson.duration_seconds * 0.8 else 'Не просмотрено',
            'viewed_time_seconds': last_viewed_time,
            'last_viewed_date': progress.created_at if last_viewed_time > 0 else None,
        })

    return Response(serialized_data)

@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
def product_statistics(request):
    print(request.user.id, '*************')
    products = models.Product.objects.filter(owner=request.user.id)




    serialized_data = []

    for product in products:
        lesson_progress = models.LessonProgress.objects.filter(lesson__products=product)
        total_viewed_lessons = lesson_progress.filter(status='viewed').count()
        total_viewed_time = sum(progress.viewed_time_seconds for progress in lesson_progress)
        total_students = models.User.objects.filter(lessonprogress__lesson__products=product).distinct().count()
        # access_count = product.user_set.count()
        # purchase_percentage = (access_count / total_students) * 100 if total_students > 0 else 0

        serialized_data.append({
            'product_id': product.id,
            'product_name': product.name,
            'total_viewed_lessons': total_viewed_lessons,
            'total_viewed_time_seconds': total_viewed_time,
            'total_students': total_students,
            # 'access_count': access_count,
            # 'purchase_percentage': purchase_percentage,
        })

    return Response(serialized_data)









