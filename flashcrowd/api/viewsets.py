from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
        task = get_object_or_404(Task, pk=pk)

        if Call.objects.filter(task=task, executor=request.user).count():
            # What the fuck? The user tries to accept the task AGAIN? Not on my watch!
            raise APIException('You cannot accept the task again, retard!')

        call = Call(task=task, executor=request.user, is_accepted=True)
        call.save()

        ser = serializers.CallSerializer(instance=call)
        return Response(ser.data)
