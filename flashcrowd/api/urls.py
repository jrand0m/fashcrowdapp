from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/', views.create_task, name='create'),
    url(r'^accept/', views.accept_task, name='accept'),
    url(r'^reject/', views.reject_task, name='reject')
]
