from logging import error

from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from todos.serializers import CreateSerializer


def create(request):
    data = JSONParser().parse(request)
    serializer = CreateSerializer(data=data, context={
        'request': request
    })
    if serializer.is_valid():
        serializer.save()
        response = JsonResponse(serializer.data, status=201)
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
