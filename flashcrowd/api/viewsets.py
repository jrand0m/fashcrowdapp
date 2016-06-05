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
from flashcrowd.core.models import Task, Call, Badge, Event, Category, UserBadge, Bookmark
from django.utils.timezone import datetime
import pytz


class UsersViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.UserModelPermission]

    @list_route(permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(self.serializer_class(instance=request.user, many=False, context=dict(request=request)).data)


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

            Event.create_new('task_accepted' if is_accept else 'task_rejected', [task.author])

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

        Event.create_new('task_completed', [task.author])

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

    @list_route(permission_classes=[IsAuthenticated])
    def add_to_bookmark(self, request, pk):
        task = get_object_or_404(Task, pk=pk, task__author=request.user)
        Bookmark.objects.create_new()



class CallsViewSet(ModelViewSet):
    serializer_class = serializers.CallSerializer
    permission_classes = [permissions.CallModelPermission]

    def get_queryset(self):
        return Call.objects.filter(task__author=self.request.user, state='completed')

    @detail_route(permission_classes=[IsAuthenticated])
    def approve(self, request, pk):
        call = get_object_or_404(Call, pk=pk, task__author=request.user)

        if call.state != 'completed':
            raise APIException('Cannot approve task if call state is "{}" (must be "completed").'.format(
                call.state
            ))

        call.state = 'won'
        call.save()

        call.executor.grant_points(call.task.get_final_bounty())

        Event.create_new('proof_accepted', [call.executor])

        return Response(serializers.CallSerializer(instance=call, many=False, context=dict(request=request)).data)

    @detail_route(permission_classes=[IsAuthenticated])
    def decline(self, request, pk):
        call = get_object_or_404(Call, pk=pk, task__author=request.user)

        if call.state != 'completed':
            raise APIException('Cannot decline task if call state is "{}" (must be "completed").'.format(
                call.state
            ))

        call.state = 'lost'
        call.save()

        Event.create_new('proof_rejected', [call.executor])

        return Response(serializers.CallSerializer(instance=call, many=False, context=dict(request=request)).data)


class BadgesViewSet(ModelViewSet):
    serializer_class = serializers.BadgeSerializer
    permission_classes = [permissions.BadgeModelPermission]
    queryset = Badge.objects.all()


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


class UserBadgesViewSet(ModelViewSet):
    serializer_class = serializers.UserBadgesSerializer
    permission_classes = [permissions.UserBadgeModelPermission]

    def get_queryset(self):
        user = self.request.user
        all_badges = Badge.objects.all()
        user_calls = Call.objects.filter(executor=user.id)
        user_tasks = Task.objects.filter(id__in=[call.task.id for call in user_calls])
        exclude_badges_list = [ub.badge for ub in UserBadge.objects.filter(user=user.id)]

        for badge in all_badges:
            if badge not in exclude_badges_list:
                try:
                    if eval(badge.validator, globals(), locals()):
                        UserBadge.objects.create(user=user, badge=badge, award_date=datetime.now())
                        try:
                            icon = badge.icon.url
                        except:
                            icon = None
                        Event.create_new('badge_earned', [user], dict(
                            icon=icon,
                            name=badge.name
                        ))
                except TypeError as e:
                    print "error!  i know - very informative. probably bad validation badge id {}. error is {}".format(badge.id, e)
        return UserBadge.objects.filter(user=user.id)


class BookmarksViewSet(ModelViewSet):
    serializer_class = serializers.BookmarksSerializer
    permission_classes = [permissions.BookmarksModelPermission]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user.id)
