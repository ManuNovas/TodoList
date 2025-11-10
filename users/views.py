from logging import error

from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser

from users.serializers import RegisterSerializer, LoginSerializer


def get_or_create_token(user):
    return Token.objects.get_or_create(user=user)[0].key

# Create your views here.
@csrf_exempt
def register(request):
    try:
        if request.method != 'POST':
            return HttpResponse('Method not allowed', status=405)
        data = JSONParser().parse(request)
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.instance
            response = JsonResponse({
                'token': get_or_create_token(user)
            }, status=200)
        else:
            response = JsonResponse(serializer.errors, status=400)
    except Exception as e:
        error(e)
        response = HttpResponse('Internal server error', status=500)
    return response


@csrf_exempt
def login(request):
    try:
        if request.method != 'POST':
            return HttpResponse('Method not allowed', status=405)
        data = JSONParser().parse(request)
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        user = authenticate(username=serializer.data['email'], password=serializer.data['password'])
        if user is None:
            return HttpResponse('Invalid credentials', status=401)
        response = JsonResponse({
            'token': get_or_create_token(user)
        }, status=200)
    except Exception as e:
        error(e)
        response = HttpResponse('Internal server error', status=500)
    return response
