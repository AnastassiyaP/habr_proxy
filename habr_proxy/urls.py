from django.urls import re_path

from . import views


urlpatterns = [
	re_path('(?P<path>.*)', views.habr_proxy),
]
