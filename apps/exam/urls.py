from django.urls import path

from main_app.urls import API_V1
from .views import ReportsView, orientation_view, ExamViewSet

app_name = 'exam'

urlpatterns = [
    path('reports/', ReportsView.as_view(), name='reports'),
    path('orientation/', orientation_view, name='orientation'),
]

API_V1.register(
    r'exams',
    ExamViewSet,
    basename='exam'
)
