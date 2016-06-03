from rest_framework.serializers import ModelSerializer
from flashcrowd.users.models import CustomUser
from flashcrowd.core.models import Task, Call


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'photo', 'points')


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
