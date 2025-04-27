import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.tweets.models import Tweet, TweetFiles


@csrf_exempt
@require_POST
def api_create_tweet(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=401)

    try:
        # Obtener el contenido crudo
        raw_content = request.POST.get('content', '').strip()

        # Convertir texto plano a formato Quill JSON válido
        if not raw_content.startswith('{') or not raw_content.endswith('}'):
            # Si no es JSON, convertirlo a formato Quill básico
            quill_content = {
                "ops": [{
                    "insert": raw_content + "\n"
                }]
            }
            content = json.dumps(quill_content)
        else:
            # Si parece JSON, validarlo
            try:
                parsed = json.loads(raw_content)
                content = raw_content  # Mantener el JSON original
            except json.JSONDecodeError:
                # Si el JSON es inválido, convertirlo a formato Quill
                quill_content = {
                    "ops": [{
                        "insert": raw_content + "\n"
                    }]
                }
                content = json.dumps(quill_content)

        # Validar que el contenido no esté vacío
        if not content or content == '{"ops": [{"insert": "\\n"}]}':
            return JsonResponse({'status': 'error', 'message': 'El contenido no puede estar vacío'}, status=400)

        # Crear el tweet
        tweet = Tweet.objects.create(
            user=request.user,
            content=content
        )

        # Procesar archivos multimedia
        for file in request.FILES.values():
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
            'received_content': raw_content
        }, status=500)