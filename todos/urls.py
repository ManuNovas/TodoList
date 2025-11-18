from django.urls import path

from todos.views import index

app_name = 'todos'
urlpatterns = [
    path('', index, name='index'),
]
