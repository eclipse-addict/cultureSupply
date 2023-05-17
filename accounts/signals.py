from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from points.models import Point, PointHistory
from points.views import new_user_point, create_point_history


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    last_login_local = timezone.localtime(user.last_login)
    current_time = timezone.localtime(timezone.now())

    if last_login_local <= current_time - timedelta(days=1):
        print('로그인 보상 있음')
        user_point, _ = Point.objects.get_or_create(user=user)
        user_point.current_points += 50
        user_point.save()
        create_point_history(50, user, '로그인', 'add')
    else:
        print('로그인 보상 없음')
