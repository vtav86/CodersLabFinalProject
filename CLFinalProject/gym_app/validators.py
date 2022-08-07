import re

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from gym_app.models import MemberNumber


def validate_member_number(value):
    if MemberNumber.objects.filter(member_number=value):
        raise ValidationError('Member Number Already In Use!')


def validate_valid_member_number(value):
    if not MemberNumber.objects.filter(member_number=value):
        raise ValidationError('Member Number Not Found!')


def validate_check_password(value):
    if len(value) < 8:
        raise ValidationError('Password needs to be minimum 8 characters')
    if not re.search('[A-Z]', value):
        raise ValidationError('Password needs to contain a capital letter')
    if not re.search('[!@#$%&()\-_[\]{};:"./<>?]', value):
        raise ValidationError('Password needs to include at least one special character from the following list - !@#$%&()\-_[\]{};:"./<>?\'')



