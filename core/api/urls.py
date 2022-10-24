from operator import index
from django.urls import path
# from .views import index, signup, signin, logout, settings, upload, like_post, profile, search
from .views import RegistrationAPIView



urlpatterns = [
    path('', RegistrationAPIView.as_view())
]


'''
urlpatterns = [
    path('', index, name='index'),
    # path('api/', IndexAPIView.as_view()),
    path('searh', search, name='search'),
    path('profile/<str:pk>', profile, name='proifle'),
    path('like-post', like_post, name='like-post'),
    path('upload', upload, name='upload'),
    path('settings', settings, name='settings'),
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('logout', logout, name='logout')
]'''