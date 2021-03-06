from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm
from .models import User
from django.views.generic.edit import UpdateView, CreateView
from django.forms.models import modelform_factory

@login_required()
def dashboard(request):
    return render(request, 'registration/dashboard.html', {})

def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html', {'form': SignUpForm})
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

class UpdateProfileView(UpdateView):
    model = User
    form_class = modelform_factory(User, fields=['first_name',
                                                 'last_name',
                                                 'bio',
                                                 'profile_picture'])
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/edit_profile.html'

