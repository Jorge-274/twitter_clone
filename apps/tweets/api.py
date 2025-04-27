import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.tweets.models import Tweet, TweetFiles

from django.utils.html import escape

@csrf_exempt
@require_POST
def api_create_tweet(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=401)

    try:
        raw_content = request.POST.get('content', '').strip()
        print(raw_content, type(raw_content), "puta madre")

        if not raw_content:
            return JsonResponse({'status': 'error', 'message': 'El contenido no puede estar vacío'}, status=400)


        print("llego aqui 2")

        tweet = Tweet.objects.create(
            user=request.user,
            content=raw_content  # GUARDAMOS HTML
        )

        print("llego aqui3")


        for file in request.FILES.getlist('media'):
            TweetFiles.objects.create(
                tweet=tweet,
                file=file,
                file_type=file.content_type.split('/')[0]
            )

        print("llego aqui4")

        return JsonResponse({
            'status': 'success',
            'tweet_id': tweet.id,
            'message': 'Tweet publicado correctamente'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f"Error en el servidor: {str(e)}",
        }, status=500)
