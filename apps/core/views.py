from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.exam.models import Exam


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        can_play_game = False
        user_exams = Exam.objects.filter(user=self.request.user)
        if (
                user_exams.filter(type=Exam.Type.visual_memory).exists() and
                user_exams.filter(type=Exam.Type.working_memory).exists() and
                user_exams.filter(type=Exam.Type.orientation).exists() and
                user_exams.filter(type=Exam.Type.perspective_taking).exists()
        ):
            can_play_game = True

        context.update({
            'can_play_game': can_play_game
        })
        return context


class HowToUseView(LoginRequiredMixin, TemplateView):
    template_name = 'core/how-to-use.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'core/terms_and_conditions.html'
