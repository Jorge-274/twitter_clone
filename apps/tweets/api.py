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
        print(raw_content, type(raw_content))

        if not raw_content:
            return JsonResponse({'status': 'error', 'message': 'El contenido no puede estar vacío'}, status=400)

        # # Si recibimos Quill JSON, ignorarlo y trabajar como texto plano
        # try:
        #     content_data = json.loads(raw_content)
        #     plain_text = ''.join(op['insert'] for op in content_data.get('ops', []) if isinstance(op.get('insert'), str))
        # except (json.JSONDecodeError, KeyError, TypeError):
        #     plain_text = raw_content

        # Ahora convertimos el texto plano a HTML sencillo
        safe_text = escape(raw_content).replace("\n", "<br>")  # Escapar y mantener saltos de línea
        content_html = f"<p>{safe_text}</p>"

        tweet = Tweet.objects.create(
            user=request.user,
            content=content_html  # GUARDAMOS HTML
        )

        for file in request.FILES.getlist('media'):
            TweetFiles.objects.create(
                tweet=tweet,
                file=file,
                file_type=file.content_type.split('/')[0]
            )

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
