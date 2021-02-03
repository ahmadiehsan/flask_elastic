from django.urls import path

from .views import HomeView, HowToUse

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('how-to-use/', HowToUse.as_view(), name='how-to-use'),
]
