from collections import OrderedDict

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route, detail_route
import serializers
import permissions
from flashcrowd.users.models import CustomUser
from flashcrowd.core.models import Task, Call, Badge, Event, Category
from django.utils.timezone import datetime
import pytz


class UsersViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.UserModelPermission]


class TasksViewSet(ModelViewSet):
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.TaskModelPermission]
    queryset = Task.objects.order_by('-date_created')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        Event.create_new('task_created', [self.request.user])
        users = list(CustomUser.objects.exclude(id=self.request.user.id).all())
        Event.create_new('new_task', users)

    def accept_or_reject(self, request, pk, is_accept):
        task = get_object_or_404(Task, pk=pk)

        call = Call.objects.filter(task=task, executor=request.user).first()

        if not call:
            call = Call(task=task, executor=request.user, state='accepted' if is_accept else 'rejected')
            call.save()

        return Response(serializers.TaskSerializer(instance=task, context=dict(request=request)).data)

    @detail_route(permission_classes=[IsAuthenticated])
    def accept(self, request, pk):
        return self.accept_or_reject(request, pk, True)

    @detail_route(permission_classes=[IsAuthenticated])
    def reject(self, request, pk):
        return self.accept_or_reject(request, pk, False)

    @detail_route(permission_classes=[IsAuthenticated], parser_classes=[FormParser, MultiPartParser], methods=['POST'])
    def complete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        proof = request.FILES.get('proof')
        if not proof:
            raise APIException('Missing proof image!')

        call = Call.objects.filter(task=task, executor=request.user).first()

        if not call:
            raise APIException('Cannot complete task before you accept or reject it.')

        if call.state != 'accepted':
            raise APIException('Cannot complete task if call state is "{}" (must be "accepted").'.format(
                call.state
            ))

        # TODO: Store proof image here
        call.state = 'completed'
        call.proof.save(proof.name, proof)
        call.save()

        return Response(serializers.TaskSerializer(instance=task, context=dict(request=request)).data)

    @list_route(permission_classes=[IsAuthenticated])
    def created_tasks(self, request):
        queryset = Task.objects.filter(author=self.request.user).order_by(
            'date_created'
        )
        return Response(serializers.TaskSerializer(instance=queryset, many=True, context=dict(request=self.request)).data)

    @list_route(permission_classes=[IsAuthenticated])
    def available_tasks(self, request):
        called_tasks = [x.task_id for x in Call.objects.filter(executor=self.request.user)]
        queryset = Task.objects.exclude(author=self.request.user).exclude(id__in=called_tasks).order_by('date_created')
        return Response(serializers.TaskSerializer(instance=queryset, many=True, context=dict(request=self.request)).data)

    @list_route(permission_classes=[IsAuthenticated])
    def active_tasks(self, request):
        called_active_tasks = [x.task_id for x in Call.objects.filter(executor=self.request.user, state__in=[
            'accepted', 'completed'
        ])]
        queryset = Task.objects.filter(id__in=called_active_tasks).order_by('date_created')
        return Response(serializers.TaskSerializer(instance=queryset, many=True, context=dict(request=self.request)).data)

    @list_route(permission_classes=[IsAuthenticated])
    def finished_tasks(self, request):
        called_active_tasks = [x.task_id for x in Call.objects.filter(executor=self.request.user, state__in=[
            'won', 'lost'
        ])]
        queryset = Task.objects.filter(id__in=called_active_tasks).order_by('date_created')
        return Response(serializers.TaskSerializer(instance=queryset, many=True, context=dict(request=self.request)).data)

    def list(self, request, *args, **kwargs):
        return Response(OrderedDict((
            ('created_tasks', reverse('task-created-tasks', request=self.request)),
            ('available_tasks', reverse('task-available-tasks', request=self.request)),
            ('active_tasks', reverse('task-active-tasks', request=self.request)),
            ('finished_tasks', reverse('task-finished-tasks', request=self.request)),
        )), status=400)


class CallsViewSet(ModelViewSet):
    serializer_class = serializers.CallSerializer
    permission_classes = [permissions.CallModelPermission]

    def get_queryset(self):
        return Call.objects.filter(executor=self.request.user, state='completed')

    @detail_route(permission_classes=[IsAuthenticated])
    def approve(self, request, pk):
        call = get_object_or_404(Call, pk=pk, task__author=request.user)

        call.state = 'won'
        call.save()

        return Response(serializers.CallSerializer(instance=call, many=False, context=dict(request=request)).data)

    @detail_route(permission_classes=[IsAuthenticated])
    def decline(self, request, pk):
        call = get_object_or_404(Call, pk=pk, task__author=request.user)

        call.state = 'lost'
        call.save()

        return Response(serializers.CallSerializer(instance=call, many=False, context=dict(request=request)).data)


class BadgesViewSet(ModelViewSet):
    serializer_class = serializers.BadgeSerializer
    permission_classes = [permissions.BadgeModelPermission]

    def get_queryset(self):
        return Badge.objects.all()


class EventsViewSet(ModelViewSet):
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
    permission_classes = [permissions.EventModelPermission]

    def get_queryset(self):
        min = float(self.request.GET.get('min', 0)) / 1000000

        local_tz = pytz.timezone("Europe/Kiev")
        utc_dt = datetime.utcfromtimestamp(min).replace(tzinfo=pytz.utc)
        local_dt = local_tz.normalize(utc_dt.astimezone(local_tz))

        return Event.objects.filter(target_users=self.request.user, date_created__gt=local_dt).order_by('-date_created')


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.CategoryModelPermission]

