from django.urls import path

from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='create'),
    path('<int:img_id>/<slug:slug>/', views.image_detail, name='detail'),
]