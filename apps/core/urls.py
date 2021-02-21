from django.urls import path

from .views import HomeView, HowToUseView, TermsAndConditionsView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('how-to-use/', HowToUseView.as_view(), name='how-to-use'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
]
