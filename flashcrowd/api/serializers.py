from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedRelatedField
from flashcrowd.users.models import CustomUser
from flashcrowd.core.models import Task, Call, Badge, UserBadge


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'photo', 'points', 'badges_earned')
        #fields = ('id', 'url', 'username', 'first_name', 'last_name', 'photo', 'points', 'badges_earned')

    badges_earned = SerializerMethodField()
    # badges = BadgeSerializer(many=True, read_only=True, queryset=)

    def get_badges_earned(self, obj):
        #TODO mike: dont know how not to include all badges
        user_badge_ids = [ub.badge_id for ub in UserBadge.objects.filter(user=obj)]
        queryset = Badge.objects.filter(id__in=user_badge_ids)
        return BadgeSerializer(instance=queryset, context=self.context, many=True).data
        #return obj.calls.filter(state='failed').count()


class CallSerializer(ModelSerializer):
    class Meta:
        model = Call
        fields = ('id', 'date_decided', 'state', 'proof', 'task', 'executor')

    # task = SerializerMethodField()

    # task = TaskSerializer(many=False)

    task = HyperlinkedRelatedField(view_name='task-detail', read_only=True)
    executor = UserSerializer(many=False)

    # def get_task(self, obj):
    #     return TaskSerializer(instance=obj.task, many=False).data


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id', 'url', 'description', 'date_created', 'date_deadline', 'bounty', 'author', 'calls',
            'calls_total', 'calls_accepted', 'calls_completed', 'calls_succeeded', 'calls_failed'
        )
        read_only_fields = ('id', 'url', 'date_created', 'author', 'calls', 'calls_total')

    author = UserSerializer(many=False, read_only=True)

    calls_total = SerializerMethodField(read_only=True)
    calls_accepted = SerializerMethodField(read_only=True)
    calls_completed = SerializerMethodField(read_only=True)
    calls_succeeded = SerializerMethodField(read_only=True)
    calls_failed = SerializerMethodField(read_only=True)

    # calls = SerializerMethodField()

    # calls = CallSerializer(instance=Call.objects.order_by('date_decided'), many=True)
    calls = CallSerializer(many=True, read_only=True)

    def get_calls_total(self, obj):
        return obj.calls.count()

    def get_calls_accepted(self, obj):
        return obj.calls.filter(state='accepted').count()

    def get_calls_completed(self, obj):
        return obj.calls.filter(state='completed').count()

    def get_calls_succeeded(self, obj):
        return obj.calls.filter(state='succeeded').count()

    def get_calls_failed(self, obj):
        return obj.calls.filter(state='failed').count()


class BadgeSerializer(ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'icon', 'name', 'description')
