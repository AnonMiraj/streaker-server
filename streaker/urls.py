from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('trainees/', views.TraineeListCreateView.as_view(), name='trainee-list'),
    path('trainees/<str:pk>/', views.TraineeDetailUpdateDestroyView.as_view(), name='trainee-detail'),
    path('records/', views.TraineeRecordListCreateView.as_view(), name='record-list'),
    path('records/<int:pk>/', views.TraineeRecordDetailUpdateDestroyView.as_view(), name='record-detail'),
    path('admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)
