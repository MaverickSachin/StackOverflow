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
]
