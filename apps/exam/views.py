import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .forms import CurrentStatusForm
from .models import Exam
from .serializers import ExamSerializer


@login_required
def current_status_view(request):
    user = request.user
    form = CurrentStatusForm(user=user)
    success = 'false'
    already_taken = 'false'
    result = {}

    try:
        exam = Exam.objects.get(user=user, type=Exam.Type.current_status)
        already_taken = 'true'
        result = json.loads(exam.result)
    except:
        pass

    if request.method == 'POST':
        form = CurrentStatusForm(user=user, data=request.POST)
        if form.is_valid():
            final_point = 0
            questions = {
                'one': {
                    'answer': '1',
                    'point': 2
                },
                'two': {
                    'answer': '2',
                    'point': 2
                }
            }
            for q, a in form.cleaned_data.items():
                question = questions[q]
                if question['answer'] == a:
                    final_point += question['point']

            try:
                Exam.objects.create(
                    user=user,
                    type=Exam.Type.current_status,
                    result=json.dumps({'final_point': final_point})
                )
                success = 'true'
                result = {'final_point': final_point}
            except:
                pass

    return render(
        request,
        'exam/current_status.html',
        {
            'form': form,
            'success': success,
            'result': result,
            'already_taken': already_taken
        }
    )


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'exam/reports.html'


class ExamViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
