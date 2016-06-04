from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
import serializers
import permissions
from flashcrowd.users.models import CustomUser
from flashcrowd.core.models import Task, Call, Badge


class UsersViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.UserModelPermission]


class TasksViewSet(ModelViewSet):
    serializer_class = serializers.TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.TaskModelPermission]

    def accept_or_reject(self, request, pk, is_accept):
        task = get_object_or_404(Task, pk=pk)

        if Call.objects.filter(task=task, executor=request.user).count():
            # What the fuck? The user tries to accept the task AGAIN? Not on my watch!
            raise APIException('You cannot accept/reject the task again, retard!')

        call = Call(task=task, executor=request.user, state='accepted' if is_accept else 'rejected')
        call.save()

        return Response(serializers.CallSerializer(instance=call, context=dict(request=request))).data

    @detail_route(permission_classes=[IsAuthenticated])
    def accept(self, request, pk):
        return self.accept_or_reject(request, pk, True)

    @detail_route(permission_classes=[IsAuthenticated])
    def reject(self, request, pk):
        return self.accept_or_reject(request, pk, False)

    @detail_route(permission_classes=[IsAuthenticated])
    def complete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        call = Call.objects.filter(task=task, executor=request.user).first()

        if not call:
            raise APIException('Cannot complete task before you accept or reject it.')

        if call.state != 'accepted':
            raise APIException('Cannot complete task if call state is "{}" (must be "accepted").'.format(
                call.state
            ))

        # TODO: Store proof image here
        call.state = 'completed'
        call.save()

        return Response(serializers.TaskSerializer(instance=task, context=dict(request=request)).data)


class CallsViewSet(ModelViewSet):
    serializer_class = serializers.CallSerializer
    queryset = Call.objects.all()
    permission_classes = [permissions.CallModelPermission]


class BadgesViewSet(ModelViewSet):
    serializer_class = serializers.BadgeSerializer
    queryset = Badge.objects.all()
    permission_classes = [permissions.BadgeModelPermission]
