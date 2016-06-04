from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedRelatedField
from flashcrowd.users.models import CustomUser
from flashcrowd.core.models import Task, Call, Badge


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'photo', 'points')
        #fields = ('id', 'url', 'username', 'first_name', 'last_name', 'photo', 'points', 'badges_earned')

    #badges_earned = SerializerMethodField()
    #badges = BadgeSerializer(many=True, read_only=True)

    def badges_earned(self, obj):
        #TODO mike: dont know how not to include all badges
        return obj.badges.filter(state='failed')
        raise NotImplementedError()
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
            'id', 'url', 'date_created', 'date_deadline', 'bounty', 'author', 'calls',
            'calls_total', 'calls_accepted', 'calls_completed', 'calls_succeeded', 'calls_failed'
        )

    author = UserSerializer(many=False)

    calls_total = SerializerMethodField()
    calls_accepted = SerializerMethodField()
    calls_completed = SerializerMethodField()
    calls_succeeded = SerializerMethodField()
    calls_failed = SerializerMethodField()

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






