"""Users views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect

# Models
from django.contrib.auth.models import User
from users.models import Profile

# Forms
from users.forms import UserForm

class LoginView(auth_views.LoginView):
    """Login view."""
    template_name = 'users/login.html'

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""
    template_name = 'users/login.html'

class ProfileDetailView(LoginRequiredMixin, UpdateView):
    """Profile view."""
    template_name = 'users/profile.html'
    model = User
    form_class = UserForm

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        """Add detection's notes to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['profile'] = Profile.objects.get(user=user)
        context['segment'] = 'profile'
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse("users:profile")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        user = self.get_object()

        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        userupate = User.objects.filter(pk=user.pk).update(username=username,email=email,first_name=first_name,last_name=last_name)

        phone = request.POST['phone_number']

        profile = Profile.objects.filter(user=user).update(phone_number=phone)

        if len(request.FILES) != 0:
            picture = request.FILES['picture']
            profile = Profile.objects.get(user=user)
            profile.picture = picture
            profile.save()

        return redirect('users:profile')
