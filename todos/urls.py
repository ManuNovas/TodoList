from django.urls import path

from todos.views import index, item

app_name = 'todos'
urlpatterns = [
    path('', index, name='index'),
    path('<int:primary_key>', item, name='item')
]
