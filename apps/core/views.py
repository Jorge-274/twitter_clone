from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import Count

from apps.tweets.models import Tweet
from apps.users.models import UserFollow, User


@login_required
def home(request):
    # Obtener tweets de los usuarios que sigue el usuario actual y los suyos propios
    following_users = UserFollow.objects.filter(follower=request.user).values_list('following', flat=True)
    tweets = Tweet.objects.filter(
        user__in=following_users
    ).order_by('-created_at').select_related('user').prefetch_related('likes')

    # Obtener sugerencias de usuarios para seguir (excluyendo los que ya sigue)
    suggested_users = User.objects.exclude(
        id__in=following_users
    ).exclude(
        id=request.user.id
    ).annotate(
        followers_count=Count('followers')
    ).order_by('-followers_count')[:3]

    # Datos de tendencias (puedes reemplazar esto con un modelo real si lo necesitas)
    trends = [
        {'category': 'Tecnología', 'name': '#Django', 'tweets': '12.5K'},
        {'category': 'Entretenimiento', 'name': '#PremiosTV', 'tweets': '45.2K'},
        {'category': 'Deportes', 'name': '#ChampionsLeague', 'tweets': '89.7K'},
        {'category': 'Política', 'name': 'Elecciones 2023', 'tweets': '32.1K'},
        {'category': 'Tendencia en Argentina', 'name': '#Messi', 'tweets': '150K'},
    ]

    context = {
        'tweets': tweets,
        'suggested_users': suggested_users,
        'trends': trends,
    }

    return render(request, 'tweets/home.html', context)
