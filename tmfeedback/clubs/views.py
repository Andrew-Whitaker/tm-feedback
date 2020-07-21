from django.shortcuts import render
from django.views.generic import ListView

from .models import Club


class ClubIndexView(ListView):
    model = Club
    context_object_name = 'clubs'
    template_name = 'clubs/club_index.html'
