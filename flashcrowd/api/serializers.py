from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedRelatedField, RelatedField, SlugRelatedField
from flashcrowd.users.models import CustomUser
from flashcrowd.core.models import Task, Call, Badge, UserBadge, Event, Category, Bookmark
from django.utils.timezone import datetime
import time


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'icon')

    def to_representation(self, instance):
        return dict(
            id="",
            name=""
        )


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'url',
            'username', 'first_name', 'last_name', 'display_name',
            'photo', 'photo_url', 'points', 'badges_earned', 'display_name'
        )
        read_only = ('points',)
        #fields = ('id', 'url', 'username', 'first_name', 'last_name', 'photo', 'points', 'badges_earned')

    badges_earned = SerializerMethodField(read_only=True)

    def get_badges_earned(self, obj):
        #TODO mike: dont know how not to include all badges
        user_badge_ids = [ub.badge_id for ub in UserBadge.objects.filter(user=obj)]
        queryset = Badge.objects.filter(id__in=user_badge_ids)
        return BadgeSerializer(instance=queryset, context=self.context, many=True).data

    display_name = SerializerMethodField()
    photo_url = SerializerMethodField()

    def get_display_name(self, obj):
        return obj.get_display_name()

    def get_photo_url(self, obj):
        return obj.get_photo_url()


class CallSerializer(ModelSerializer):
    class Meta:
        model = Call
        fields = ('id', 'date_decided', 'state', 'proof', 'task', 'executor')

    task = SerializerMethodField()

    # task = TaskSerializer(many=False)

    # task = HyperlinkedRelatedField(view_name='task-detail', read_only=True)
    executor = UserSerializer(many=False)

    # def get_task(self, obj):
    #     return TaskSerializer(instance=obj.task, many=False).data
    def get_task(self, obj):
        return DeepTaskSerializer(instance=obj.task, many=False, context=self.context).data


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id', 'url', 'category', 'description', 'date_created', 'date_deadline', 'bounty', 'author', 'is_author',
            'call', 'calls', 'summary', 'calls_total', 'calls_accepted', 'calls_completed', 'calls_succeeded', 'calls_failed'
        )
        read_only_fields = ('id', 'url', 'date_created', 'author', 'calls', 'calls_total')

    author = UserSerializer(many=False, read_only=True)
    category = SlugRelatedField(slug_field='slug', read_only=False, queryset=Category.objects.all())

    # category = CategorySerializer(many=False)
    # category = RelatedField(queryset=Category.objects.all())

    calls_total = SerializerMethodField(read_only=True)
    calls_accepted = SerializerMethodField(read_only=True)
    calls_completed = SerializerMethodField(read_only=True)
    calls_succeeded = SerializerMethodField(read_only=True)
    calls_failed = SerializerMethodField(read_only=True)

    calls = HyperlinkedRelatedField(view_name='call-detail', read_only=True, many=True)

    # calls = SerializerMethodField()

    # calls = CallSerializer(instance=Call.objects.order_by('date_decided'), many=True)
    # calls = CallSerializer(many=True, read_only=True)

    is_author = SerializerMethodField(read_only=True)
    call = SerializerMethodField(read_only=True)

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

    def get_is_author(self, obj):
        return obj.author.id == self.context['request'].user.id

    def get_call(self, obj):
        call = Call.objects.filter(executor=self.context['request'].user, task=obj).first()
        if not call:
            return None
        return DeepCallSerializer(instance=call, many=False, context=self.context).data

class BadgeSerializer(ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'url', 'icon', 'name', 'description', 'level')


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'url', 'type', 'style', 'message', 'date')

    date = SerializerMethodField()

    def get_date(self, obj):
        epoch = datetime.utcfromtimestamp(0)
        return int((obj.date_created.replace(tzinfo=None) - epoch).total_seconds() * 1000000)
        # return int(time.mktime(obj.date_created.timetuple()) * 1000)


class DeepTaskSerializer(TaskSerializer):
    calls = HyperlinkedRelatedField(view_name='call-detail', read_only=True, many=True)

    def get_call(self, obj):
        call = Call.objects.filter(executor=self.context['request'].user, task=obj).first()
        if not call:
            return None
        return reverse('call-detail', args=(call.id,), request=self.context['request'])


class DeepCallSerializer(CallSerializer):
    task = HyperlinkedRelatedField(view_name='task-detail', read_only=True)


class UserBadgesSerializer(ModelSerializer):
    class Meta:
        model = UserBadge
        fields = ('id', 'user', 'badge', 'award_date')

    badge = BadgeSerializer(many=False, read_only=True)


class BookmarksSerializer(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'user', 'task')

