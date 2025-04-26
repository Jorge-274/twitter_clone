from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.tweets.models import Tweet
from apps.users.models import User, UserFollow


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