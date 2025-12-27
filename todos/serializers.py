from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import Serializer

from todos.models import ToDo

DEFAULT_PAGE = 1
DEFAULT_LIMIT = 10


class ItemSerializer(Serializer):
    id = IntegerField(read_only=True)
    title = CharField(max_length=128, required=True)
    description = CharField(max_length=1024, required=True)

    def create(self, validated_data):
        user = self.context['request'].user
        return ToDo.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ListSerializer(Serializer):
    page = IntegerField(default=DEFAULT_PAGE)
    limit = IntegerField(default=DEFAULT_LIMIT)
