from logging import error

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from todos.models import ToDo
from todos.serializers import ItemSerializer, ListSerializer, DEFAULT_LIMIT, DEFAULT_PAGE


def create(request):
    data = JSONParser().parse(request)
    serializer = ItemSerializer(data=data, context={
        'request': request,
    })
    if serializer.is_valid():
        serializer.save()
        response = JsonResponse(serializer.data, status=201)
    else:
        response = JsonResponse(serializer.errors, status=400)
    return response


def update(request, todo: ToDo):
    data = JSONParser().parse(request)
    serializer = ItemSerializer(todo, data=data)
    if serializer.is_valid():
        serializer.save()
        response = JsonResponse(serializer.data, status=200)
    else:
        response = JsonResponse(serializer.errors, status=400)
    return response


def delete(todo: ToDo):
    todo.delete()
    return HttpResponse(status=204)


def get(request):
    serializer = ListSerializer(data=request.GET)
    if serializer.is_valid():
        todos = ToDo.objects.filter(user=request.user)
        search = serializer.validated_data.get('search', None)
        if search is not None:
            todos = todos.filter(Q(title__icontains=search) | Q(description__icontains=search))
        sort_by = serializer.validated_data.get('sort_by', 'id')
        order = serializer.validated_data.get('order', 'asc')
        todos = todos.order_by(f'{'-' if order == 'desc' else ''}{sort_by}')
        limit = serializer.validated_data.get('limit', DEFAULT_LIMIT)
        paginator = Paginator(todos, limit)
        page = serializer.validated_data.get('page', DEFAULT_PAGE)
        data = paginator.get_page(page)
        items = ItemSerializer(data.object_list, many=True)
        response = JsonResponse({
            'data': items.data,
            'page': page,
            'limit': limit,
            'total': paginator.count,
        }, status=200, safe=False)
    else:
        response = JsonResponse(serializer.errors, status=400)
    return response


# Create your views here.
@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    try:
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        if request.method == 'POST':
            response = create(request)
        elif request.method == 'GET':
            response = get(request)
        else:
            response = HttpResponse('Method not allowed', status=405)
    except Exception as e:
        error(e)
        response = HttpResponse('Internal server error', status=500)
    return response


@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def item(request, primary_key: int):
    try:
        todo = ToDo.objects.get(pk=primary_key, user=request.user)
        if request.method == 'PUT':
            response = update(request, todo)
        elif request.method == 'DELETE':
            response = delete(todo)
        else:
            response = HttpResponse('Method not allowed', status=405)
    except Exception as e:
        error(e)
        if e.__class__.__name__ == 'DoesNotExist':
            response = HttpResponse('ToDo not found', status=404)
        else:
            response = HttpResponse('Internal server error', status=500)
    return response
