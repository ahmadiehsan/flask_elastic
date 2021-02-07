import json
from statistics import mean

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from .forms import OrientationForm
from .models import Exam
from .serializers import ExamSerializer


@login_required
def orientation_view(request):
    user = request.user
    form = OrientationForm()
    success = 'false'
    already_taken = False
    result = {}
    previous_result_html = ''

    previous_exams = Exam.objects.filter(user=user, type=Exam.Type.orientation)
    if previous_exams.count() > 0:
        already_taken = True
        for exam in previous_exams:
            previous_result_html += '{}: <span class="ps-3"><b>{}</b> points</span></br>'.format(
                exam.create_time_formatted,
                str(json.loads(exam.result)['total'])
            )

    if request.method == 'POST':
        form = OrientationForm(data=request.POST)
        if form.is_valid():
            answers = []
            total = 0
            for _, answer in form.cleaned_data.items():
                answer = int(answer)
                answers.append(answer)
                total += answer

            try:
                result = {
                    'answers': answers,
                    'total': total
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
            'previous_result_html': previous_result_html,
        }
    )


class AllExamsView(LoginRequiredMixin, TemplateView):
    template_name = 'exam/all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        already_taken_visual_memory = False
        already_taken_working_memory = False
        already_taken_orientation = False
        already_taken_perspective_taking = False

        user_exams = Exam.objects.filter(user=self.request.user)
        visual_memory_tries = user_exams.filter(type=Exam.Type.visual_memory).count()
        working_memory_tries = user_exams.filter(type=Exam.Type.working_memory).count()
        orientation_tries = user_exams.filter(type=Exam.Type.orientation).count()
        perspective_taking_tries = user_exams.filter(type=Exam.Type.perspective_taking).count()

        if visual_memory_tries > 0:
            already_taken_visual_memory = True

        if working_memory_tries > 0:
            already_taken_working_memory = True

        if orientation_tries > 0:
            already_taken_orientation = True

        if perspective_taking_tries > 0:
            already_taken_perspective_taking = True

        context.update({
            'already_taken_visual_memory': already_taken_visual_memory,
            'visual_memory_tries': visual_memory_tries,

            'already_taken_working_memory': already_taken_working_memory,
            'working_memory_tries': working_memory_tries,

            'already_taken_orientation': already_taken_orientation,
            'orientation_tries': orientation_tries,

            'already_taken_perspective_taking': already_taken_perspective_taking,
            'perspective_taking_tries': perspective_taking_tries,
        })
        return context


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'exam/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'game_result': self._prepare_game_result(),
            'game_speed': self._prepare_game_speed(),
            'performance': self._prepare_performance()
        })
        return context

    def _prepare_game_result(self):
        user = self.request.user

        show = False
        best_score = None
        accuracy = None
        best_speed = None

        coins_list = []
        accuracy_list = []
        speed_list = []
        game_history = user.exams.filter(type=Exam.Type.game)[:10]
        if game_history.exists():
            show = True

            for game in game_history:
                game_result = json.loads(game.result)
                coins_list.append(game_result['coins'])
                accuracy_list.append(game_result['accuracy'])
                speed_list.append(game_result['speed'])

            best_score = max(coins_list)
            accuracy = mean(accuracy_list)
            best_speed = min(speed_list)

        return {
            'show': show,
            'data': {
                'best_score': best_score,
                'accuracy': accuracy,
                'best_speed': best_speed,
            }
        }

    def _prepare_game_speed(self):
        user = self.request.user

        show = False
        speed_list = []

        game_history = user.exams.filter(type=Exam.Type.game)[:10]
        if game_history.exists():
            show = True

            for game in game_history:
                game_result = json.loads(game.result)
                speed_list.append(game_result['speed'])

        return {
            'show': show,
            'data': {
                'speed_list': speed_list
            }
        }

    def _prepare_performance(self):
        user = self.request.user

        show = False
        visual_memory_result = {}
        working_memory_result = {}
        orientation_result = {}
        perspective_taking_result = {}

        speed_list = []
        if user.exams.exists():
            show = True

            try:
                last_visual_memory = user.exams.filter(type=Exam.Type.visual_memory).last()
                visual_memory_result = json.loads(last_visual_memory.result)
                speed_list.append(visual_memory_result['speed'])
            except Exam.DoesNotExist:
                pass

            try:
                last_working_memory = user.exams.filter(type=Exam.Type.working_memory).last()
                working_memory_result = json.loads(last_working_memory.result)
                speed_list.append(working_memory_result['speed'])
            except Exam.DoesNotExist:
                pass

            try:
                last_orientation = user.exams.filter(type=Exam.Type.orientation).last()
                orientation_result = json.loads(last_orientation.result)
            except Exam.DoesNotExist:
                pass

            try:
                last_perspective_taking = user.exams.filter(type=Exam.Type.perspective_taking).last()
                perspective_taking_result = json.loads(last_perspective_taking.result)
                speed_list.append(perspective_taking_result['speed'])
            except Exam.DoesNotExist:
                pass

        if speed_list:
            speed = mean(speed_list)
        else:
            speed = 0

        return {
            'show': show,
            'data': {
                'visual_memory': visual_memory_result.get('memory_span', 0),
                'working_memory': working_memory_result.get('memory_span', 0),
                'orientation': orientation_result.get('total', 0),
                'perspective_taking': perspective_taking_result.get('angle', 0),
                'speed': speed
            }
        }


class ExamViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    permission_classes = (IsAdminUser,)
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
