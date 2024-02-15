from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [

    path('trainees/', views.trainee_list.as_view()),
    path('trainees/<str:pk>/', views.trainee_detail.as_view()),
    path('records/', views.trainee_record_list.as_view()),
    path('records/<int:pk>/', views.trainee_record_detail.as_view()),

    path('admin/', admin.site.urls),
]
urlpatterns = format_suffix_patterns(urlpatterns)
