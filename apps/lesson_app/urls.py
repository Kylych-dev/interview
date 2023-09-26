from django.urls import path
from . import views

urlpatterns = [
    path('userles/', views.user_lessons, name='user_lessons'),
    # path('user_lessons/', views.user_products, name='user_lessons'),
    path('prodles/<int:product_id>/', views.lessons_list, name='product_lessons'),
    path('prodstat/', views.product_statistics, name='product_statistics'),
]
