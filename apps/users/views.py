from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.tweets.models import Tweet
from apps.users.models import User, UserFollow
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import LoginForm


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido de nuevo, @{username}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})



def users_home(request):
    return HttpResponse("Página principal de Users")


from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView



class ProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['tweets'] = Tweet.objects.filter(user=user).order_by('-created_at')
        context['is_following'] = self.request.user.is_authenticated and \
                                  self.request.user.following.filter(following=user).exists()
        return context





@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.user == user_to_follow:
        messages.error(request, "No puedes seguirte a ti mismo.")
    elif not UserFollow.objects.filter(follower=request.user, following=user_to_follow).exists():
        UserFollow.objects.create(follower=request.user, following=user_to_follow)
        messages.success(request, f"Ahora sigues a @{username}")

    return redirect('profile', username=username)


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)

    if request.user == user_to_unfollow:
        messages.error(request, "No puedes dejar de seguirte a ti mismo.")
    else:
        follow_relationship = UserFollow.objects.filter(
            follower=request.user,
            following=user_to_unfollow
        ).first()

        if follow_relationship:
            follow_relationship.delete()
            messages.success(request, f"Has dejado de seguir a @{username}")
        else:
            messages.warning(request, f"No estabas siguiendo a @{username}")

    return redirect('profile', username=username)


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            # Crear el usuario
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Loguear al usuario después del registro
            login(request, user)

            return redirect('home')  # O la página a la que quieras redirigir al usuario

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})
