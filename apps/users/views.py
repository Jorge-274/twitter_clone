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

from . import models
from .forms import LoginForm, ProfileEditForm


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


# def profile_view(request, username):
#     profile_user = get_object_or_404(User, username=username)
#     is_following = False
#
#     if request.user.is_authenticated:
#         is_following = request.user.following.filter(id=profile_user.id).exists()
#
#     tweets = Tweet.objects.filter(user=profile_user).order_by('-created_at')
#
#     context = {
#         'profile_user': profile_user,
#         'tweets': tweets,
#         'is_following': is_following,
#     }
#
#     return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    # La vista de edición siempre trabaja con el usuario logueado
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Verificar unicidad del username
            if User.objects.filter(username=user.username).exclude(pk=user.pk).exists():
                messages.error(request, 'Este nombre de usuario ya está en uso.')
            # Verificar unicidad del email
            elif User.objects.filter(email=user.email).exclude(pk=user.pk).exists():
                messages.error(request, 'Este correo electrónico ya está en uso.')
            else:
                user.save()
                messages.success(request, 'Perfil actualizado correctamente')
                return redirect('profile', username=user.username)
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


def following_list(request, username):
    user = get_object_or_404(User, username=username)
    # Obtener los usuarios seguidos (following) a través de la relación UserFollow
    following_users = User.objects.filter(followers__follower=user)
    return render(request, 'users/following.html', {'profile_user': user, 'following': following_users})

def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    # Obtener los usuarios seguidores (follower) a través de UserFollow
    followers = User.objects.filter(following__following=user)
    return render(request, 'users/followers.html', {'profile_user': user, 'followers': followers})


from django.db.models import Q  # Importa Q desde django.db.models
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from .models import User
from .serializers import UserSearchSerializer


@api_view(['GET'])
def search_users(request):
    query = request.GET.get('q', '').strip()

    if query:
        # Busca por username o full_name
        users = User.objects.filter(
            Q(username__icontains=query) |  # Usa Q directamente
            Q(full_name__icontains=query)
        ).distinct()[:5]  # Limita a 5 resultados
    else:
        users = User.objects.none()

    serializer = UserSearchSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)