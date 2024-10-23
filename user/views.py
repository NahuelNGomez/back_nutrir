
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Profile

# Create your views here.

@login_required
def profile_detail(request, username=None):
    obj = get_object_or_404(Profile, username=username)
    
    context = {
        "object": obj,
    }
    template = 'profile_detail.html'
    return render(request, template, context)