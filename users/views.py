from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from . forms import CustomUserCreationForm, UserProfileForm
from django.views import View
from django.urls import reverse_lazy


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        # Можно добавить логику, например, автоматический вход
        return super().form_valid(form)

class UserProfileView(View):
    def get(self, request):
        return render(request, 'users/profile.html')


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user  # редактируем только текущего пользователя





