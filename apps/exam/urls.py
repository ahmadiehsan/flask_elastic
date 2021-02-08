from django.urls import path

from main_app.urls import API_V1
from .views import ReportsView, orientation_view, ExamViewSet, AllExamsView, IframeView

app_name = 'exam'

urlpatterns = [
    path('reports/', ReportsView.as_view(), name='reports'),
    path('orientation/', orientation_view, name='orientation'),
    path('iframe/<path:link>/', IframeView.as_view(), name='iframe'),
    path('all/', AllExamsView.as_view(), name='all-exams'),
]

API_V1.register(
    r'exams',
    ExamViewSet,
    basename='exam'
)
