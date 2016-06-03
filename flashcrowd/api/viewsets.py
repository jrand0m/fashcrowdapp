from rest_framework.viewsets import ModelViewSet
import serializers
import permissions
from flashcrowd.users.models import CustomUser
from flashcrowd.core.models import Task, Call


class UsersViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.UserModelPermission]


class TasksViewSet(ModelViewSet):
    serializer_class = serializers.TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.TaskModelPermission]
