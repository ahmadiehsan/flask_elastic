import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .forms import OrientationForm
from .models import Exam
from .serializers import ExamSerializer


@login_required
def orientation_view(request):
    user = request.user
    form = OrientationForm()
    success = 'false'
    already_taken = 'false'
    result = {}
    previous_results = ''

    previous_exams = Exam.objects.filter(user=user, type=Exam.Type.orientation)
    if previous_exams.count() > 0:
        already_taken = 'true'
        for exam in previous_exams:
            previous_results += str(json.loads(exam.result)['final_point'])

    if request.method == 'POST':
        form = OrientationForm(data=request.POST)
        if form.is_valid():
            final_point = 0
            for _, a in form.cleaned_data.items():
                final_point += int(a)

            try:
                result = {
                    'q_a': form.cleaned_data,
                    'final_point': final_point
                }
                Exam.objects.create(
                    user=user,
                    type=Exam.Type.orientation,
                    result=json.dumps(result)
                )
                success = 'true'
            except:
                pass

    return render(
        request,
        'exam/orientation.html',
        {
            'form': form,
            'success': success,
            'result': result,
            'already_taken': already_taken,
            'previous_results': previous_results,
        }
    )


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'exam/reports.html'


class ExamViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
