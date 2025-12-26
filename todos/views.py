from logging import error

from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from todos.models import ToDo
from todos.serializers import SaveSerializer


def create(request):
    data = JSONParser().parse(request)
    serializer = SaveSerializer(data=data, context={
        'request': request
    })
    if serializer.is_valid():
        serializer.save()
        response = JsonResponse(serializer.data, status=201)
    else:
        response = JsonResponse(serializer.errors, status=400)
    return response


def update(request, todo: ToDo):
    data = JSONParser().parse(request)
    serializer = SaveSerializer(todo, data=data)
    if serializer.is_valid():
        serializer.save()
        response = JsonResponse(serializer.data, status=200)
    else:
        response = JsonResponse(serializer.errors, status=400)
    return response


# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    try:
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        if request.method == 'POST':
            response = create(request)
        else:
            response = HttpResponse('Method not allowed', status=405)
    except Exception as e:
        error(e)
        response = HttpResponse('Internal server error', status=500)
    return response


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def item(request, primary_key: int):
    try:
        todo = ToDo.objects.get(pk=primary_key, user=request.user)
        if request.method == 'PUT':
            response = update(request, todo)
        else:
            response = HttpResponse('Method not allowed', status=405)
    except Exception as e:
        error(e)
        if e.__class__.__name__ == 'DoesNotExist':
            response = HttpResponse('ToDo not found', status=404)
        else:
            response = HttpResponse('Internal server error', status=500)
    return response
