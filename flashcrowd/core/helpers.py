from flashcrowd.core.models import Badge, Call, Task, UserBadge, Event
from django.utils.timezone import datetime


def process_badges(user):
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
                print "error!  i know - very informative. probably bad validation badge id {}. error is {}".format(
                    badge.id, e)
