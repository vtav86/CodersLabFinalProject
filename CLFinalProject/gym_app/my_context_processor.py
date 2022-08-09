from datetime import datetime

from django.contrib.auth.models import User

from gym_app.weather_info_function import get_weather
import pytz


def is_staff(request):
    if request.user.is_staff:
        return True
    else:
        return False

def my_cp(request):
    user_logged_in = request.user
    if user_logged_in.is_anonymous:
        user = 'friend!'
    else:
        user = User.objects.get(username=user_logged_in).first_name
    local_yerevan_timezone = pytz.timezone("Asia/Yerevan")
    current_yerevan_time = datetime.now(local_yerevan_timezone)
    ctx = {
        "context_now": current_yerevan_time.strftime("%I:%M %p"),
        "context_version": "1.0",
        "context_weather": get_weather(),
        "context_user": user,
        "context_admin": is_staff(request)
    }
    return ctx
