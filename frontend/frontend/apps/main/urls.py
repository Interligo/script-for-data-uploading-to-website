from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    path('', views.main, name='main'),
    path('<int:psychotherapist_id>/', views.detail, name='detail')
]
