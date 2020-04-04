from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    # /boards/
    path('', views.home, name='home'),

    # /boards/1/
    path('<int:pk>/', views.topics, name='topics'),

    # /boards/1/new/
    path('<int:pk>/new/', views.new_topic, name='new_topic'),

    # /boards/1/topics/1/
    path('<int:pk>/topics/<int:topic_pk>/', views.posts, name='posts'),

    # /boards/1/topics/1/reply/
    path('<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
]
