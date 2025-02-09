from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts_view, name='posts'),
    path('<int:post_id>/', views.post_detail_view, name='posts_detail'),
]
