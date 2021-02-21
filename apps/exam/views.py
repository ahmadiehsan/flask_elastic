import json
from datetime import timedelta
from statistics import mean

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView, View
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
            'performance': self._prepare_performance(),
            'detailed_progress': self._prepare_detailed_progress(),
            'weeks_percentage': self._prepare_weeks_percentage(),
        })
        return context

    def _prepare_weeks_percentage(self):
        user = self.request.user

        show = False

        this_week_time = 0
        last_week_time = 0
        two_weeks_ago_time = 0
        three_weeks_ago_time = 0

        if user.exams.exists():
            show = True

            some_day_in_last_week = timezone.now().date() - timedelta(days=7)

            monday_of_last_week = some_day_in_last_week - timedelta(days=(some_day_in_last_week.isocalendar()[2] - 1))
            monday_of_this_week = monday_of_last_week + timedelta(days=7)

            user_games = user.exams.filter(type=Exam.Type.game)

            this_week_games = user_games.filter(
                create_time__gte=monday_of_this_week,
            )
            for game in this_week_games:
                game_result = json.loads(game.result)
                this_week_time += game_result['time']

            last_week_games = user_games.filter(
                create_time__gte=monday_of_last_week,
                create_time__lt=monday_of_this_week
            )
            for game in last_week_games:
                game_result = json.loads(game.result)
                last_week_time += game_result['time']

            two_weeks_ago_games = user_games.filter(
                create_time__gte=monday_of_last_week - timedelta(days=7),
                create_time__lt=monday_of_last_week
            )
            for game in two_weeks_ago_games:
                game_result = json.loads(game.result)
                two_weeks_ago_time += game_result['time']

            three_weeks_ago_games = user_games.filter(
                create_time__gte=monday_of_last_week - timedelta(days=14),
                create_time__lt=monday_of_last_week - timedelta(days=7)
            )
            for game in three_weeks_ago_games:
                game_result = json.loads(game.result)
                three_weeks_ago_time += game_result['time']

        return {
            'show': show,
            'data': {
                'this_week_percentage': self._percentage(this_week_time, 40 * 60),
                'last_week_percentage': self._percentage(last_week_time, 40 * 60),
                'two_weeks_ago_percentage': self._percentage(two_weeks_ago_time, 40 * 60),
                'three_weeks_ago_percentage': self._percentage(three_weeks_ago_time, 40 * 60),
            }
        }

    def _prepare_detailed_progress(self):
        user = self.request.user

        show = False

        visual_memory_memory_span_list = []
        visual_memory_date_list = []

        orientation_total_list = []
        orientation_date_list = []

        working_memory_memory_span_list = []
        working_memory_date_list = []

        speed_speed_list = []
        speed_date_list = []

        if user.exams.exists():
            show = True

            for visual_memory in user.exams.filter(type=Exam.Type.visual_memory):
                visual_memory_result = json.loads(visual_memory.result)

                speed_speed_list.append(visual_memory_result['speed'])
                speed_date_list.append(visual_memory.create_time_formatted)

                visual_memory_memory_span_list.append(visual_memory_result['memory_span'])
                visual_memory_date_list.append(visual_memory.create_time_formatted)

            for orientation in user.exams.filter(type=Exam.Type.orientation):
                orientation_result = json.loads(orientation.result)

                orientation_total_list.append(orientation_result['total'])
                orientation_date_list.append(orientation.create_time_formatted)

            for working_memory in user.exams.filter(type=Exam.Type.working_memory):
                working_memory_result = json.loads(working_memory.result)

                speed_speed_list.append(working_memory_result['speed'])
                speed_date_list.append(working_memory.create_time_formatted)

                working_memory_memory_span_list.append(working_memory_result['memory_span'])
                working_memory_date_list.append(working_memory.create_time_formatted)

            for perspective_taking in user.exams.filter(type=Exam.Type.perspective_taking):
                perspective_taking_result = json.loads(perspective_taking.result)

                speed_speed_list.append(perspective_taking_result['speed'])
                speed_date_list.append(perspective_taking.create_time_formatted)

        return {
            'show': show,
            'data': {
                'visual_memory': {
                    'memory_span_list': visual_memory_memory_span_list,
                    'date_list': visual_memory_date_list
                },
                'orientation': {
                    'total_list': orientation_total_list,
                    'date_list': orientation_date_list
                },
                'working_memory': {
                    'memory_span_list': working_memory_memory_span_list,
                    'date_list': working_memory_date_list
                },
                'speed': {
                    'speed_list': speed_speed_list,
                    'date_list': speed_date_list
                },
            }
        }

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
        date_list = []

        game_history = user.exams.filter(type=Exam.Type.game)[:10]
        if game_history.exists():
            show = True

            for game in game_history:
                game_result = json.loads(game.result)
                speed_list.append(game_result['speed'])
                date_list.append(game.create_time_formatted)

        return {
            'show': show,
            'data': {
                'speed_list': speed_list,
                'date_list': date_list
            }
        }

    def _prepare_performance(self):
        user = self.request.user

        visual_memory_result = {}
        working_memory_result = {}
        orientation_result = {}
        perspective_taking_result = {}

        speed_list = []
        if user.exams.exists():
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
            'data': {
                'visual_memory': self._percentage(visual_memory_result.get('memory_span', 0), 10),
                'working_memory': self._percentage(working_memory_result.get('memory_span', 0), 10),
                'orientation': self._percentage(orientation_result.get('total', 0), 105),
                'perspective_taking': self._percentage(perspective_taking_result.get('angle', 0), 180),
                'speed': self._percentage(speed, 1000),
            }
        }

    @staticmethod
    def _percentage(part, whole):
        return 100 * (float(part) / float(whole))


class IframeView(LoginRequiredMixin, View):
    def get(self, request, link):
        return render(request, 'exam/iframe.html', {'link': link})


class ExamViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    permission_classes = (IsAdminUser,)
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
