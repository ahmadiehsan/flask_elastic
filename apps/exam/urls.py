from django.urls import path

from main_app.urls import API_V1
from .views import ReportsView, current_status_view, ExamViewSet

app_name = 'exam'

urlpatterns = [
    path('reports/', ReportsView.as_view(), name='reports'),
    path('current-status/', current_status_view, name='current-status'),
]

API_V1.register(
    r'exams',
    ExamViewSet,
    basename='exam'
)
