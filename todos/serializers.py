from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import Serializer

from todos.models import ToDo


class CreateSerializer(Serializer):
    id = IntegerField(read_only=True)
    title = CharField(max_length=128, required=True)
    description = CharField(max_length=1024, required=True)

    def create(self, validated_data):
        user = self.context['request'].user
        return ToDo.objects.create(user=user, **validated_data)
