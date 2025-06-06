from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

@csrf_exempt
@api_view(['GET'])
def obtener_saludo(request):
    return JsonResponse({'mensaje': 'Hola desde Django!'})