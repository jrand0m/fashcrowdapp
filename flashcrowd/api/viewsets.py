from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
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

    @detail_route(permission_classes=[IsAuthenticated])
    def accept(self, request, pk):
        print 'OK'
        task = get_object_or_404(Task, pk=pk)
        task.accept(request.user)
