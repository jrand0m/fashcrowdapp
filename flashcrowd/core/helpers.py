from flashcrowd.core.models import Badge, Call, Task, UserBadge, Event
from django.utils.timezone import datetime


def process_badges(user):
    # Fellow people of Kostylland salute you!
    all_badges = Badge.objects.all()
    user_calls = Call.objects.filter(executor=user, state__in=('completed', 'won', 'lost'))

    for badge in all_badges:
        user_badge = UserBadge.objects.filter(user=user, badge=badge).first()

        level = eval(badge.validator, globals(), locals())

        if not user_badge and level > 0:
            # User has no badge yet, but has new level
            user_badge = UserBadge.objects.create(user=user, badge=badge)
            Event.create_new('badge_earned', [user], related_object=user_badge)
        elif user_badge and user_badge.level < level:
            # Badge upgraded
            user_badge.level = level
            user_badge.save()
            Event.create_new('badge_earned', [user], related_object=user_badge)
