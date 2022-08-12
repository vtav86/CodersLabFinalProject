from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django import forms
from django.forms import ModelForm

from gym_app.models import Members, MemberNumber, EventHosts, Events
from gym_app.validators import validate_member_number, validate_valid_member_number, validate_check_password


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


CITIES = (
    ('Yerevan',
     'Yerevan'),
    ('Gyumri',
     'Gyumri'),
    ('Vanadzor',
     'Vanadzor'),
    ('Hrazdan',
     'Hrazdan'),
    ('Abovyan',
     'Abovyan'),
    ('Kapan',
     'Kapan'),
    ('Armavir',
     'Armavir'),
    ('Charentsavan',
     'Charentsavan'),
    ('Artashat',
     'Artashat'),
    ('Ashtarak',
     'Ashtarak'),
    ('Ijevan',
     'Ijevan'),
    ('Gavarr',
     'Gavarr'),
    ('Nor',
     'Nor'),
    ('Hachn',
     'Hachn'),
    ('Byureghavan',
     'Byureghavan'),
    ('Yeghegnadzor',
     'Yeghegnadzor'),
    ('Ejmiatsin', 'Ejmiatsin'),
    ('Sevan', 'Sevan'),
    ('Stepanavan', 'Stepanavan'),
    ('Masis', 'Masis'),
    ('Goris', 'Goris'),
    ('Ararat', 'Ararat'),
    ('Artik', 'Artik'),
    ('Dilijan', 'Dilijan'),
    ('Spitak', 'Spitak'),
    ('Sisian', 'Sisian'),
    ('Vedi', 'Vedi'),
    ('Alaverdi', 'Alaverdi'),
    ('Vardenis', 'Vardenis'),
    ('Martuni', 'Martuni'),
    ('Metsamor', 'Metsamor'),
    ('Yeghvard', 'Yeghvard'),
    ('Ayntap', 'Ayntap'),
    ('Akhuryan', 'Akhuryan'),
    ('Berd', 'Berd'),
    ('Vardenik', 'Vardenik'),
    ('Getashen', 'Getashen'),
    ('Tashir', 'Tashir'),
    ('Jermuk', 'Jermuk'),
    ('Jrvezh', 'Jrvezh'),
    ('Garrni', 'Garrni'),
    ('Kajaran', 'Kajaran'),
    ('Noratus', 'Noratus'),
    ('Aparan', 'Aparan'),
    ('Sardarapat', 'Sardarapat'),
    ('Karmir', 'Karmir'),
    ('Gyukh', 'Gyukh'),
    ('Oshakan', 'Oshakan'),
    ('Yeranos', 'Yeranos'),
    ('Chambarak', 'Chambarak'),
    ('Aragatsavan', 'Aragatsavan'),
    ('Maralik', 'Maralik'),
    ('Lichk', 'Lichk'),
    ('Noyemberyan', 'Noyemberyan'),
    ('Odzun', 'Odzun'),
    ('Verin', 'Verin'),
    ('Getashen', 'Getashen'),
    ('Tsovinar', 'Tsovinar'),
    ('Outside of Armenia', 'Outside of Armenia'),

)


class RegisterNewMemberForm(forms.Form):
    member_number = forms.IntegerField(max_value=9999999, required=True, validators=[validate_member_number],
                                       widget=forms.NumberInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1922, 2022), attrs={'class': 'form-control'}), required=True)
    building_number = forms.IntegerField(min_value=0, max_value=99999,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
    apartment_number = forms.IntegerField(min_value=0, max_value=99999, required=True,
                                          widget=forms.NumberInput(attrs={'class': 'form-control'}))
    street_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.ChoiceField(choices=CITIES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.IntegerField(min_value=0, max_value=999999999, required=True,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)

    emergency_contact_name = forms.CharField(max_length=60, required=True,
                                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    emergency_contact_phone_number = forms.IntegerField(min_value=0, max_value=999999999, required=True,
                                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))


class OnlineRegistrationForm(forms.Form):
    member_number = forms.IntegerField(max_value=9999999, required=True, validators=[validate_valid_member_number])
    last_name = forms.CharField(max_length=30, required=True)
    password1 = forms.CharField(min_length=8, required=True, validators=[validate_check_password],
                                widget=forms.PasswordInput, label="Enter Password*")
    password2 = forms.CharField(min_length=8, required=True, validators=[validate_check_password],
                                widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('Passwords do not match')


def get_all_members():
    choices = []
    for member in Members.objects.all():
        try:
            number = MemberNumber.objects.get(member_id=member.id)
            choices.append((member.id, (member.last_name + ', ' + member.first_name + ' ' + 'Member Number ' + str(
                number.member_number))))
        except ObjectDoesNotExist:
            continue
    return choices


class ManagePaymentForm(forms.Form):
    member = forms.ChoiceField(label='Select Member', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ManagePaymentForm, self).__init__(*args, **kwargs)
        self.fields['member'].choices = get_all_members()


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label="Current Password", max_length=20, widget=forms.PasswordInput)
    password1 = forms.CharField(label="Enter New Password*", max_length=20, widget=forms.PasswordInput,
                                validators=[validate_check_password])
    password2 = forms.CharField(label="Confirm New Password", max_length=20, widget=forms.PasswordInput,
                                validators=[validate_check_password])

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('Passwords do not match')


class EditProfileForm(forms.Form):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2022)), required=True)
    building_number = forms.IntegerField(min_value=0, max_value=99999)
    apartment_number = forms.IntegerField(min_value=0, max_value=99999, required=True)
    street_name = forms.CharField(max_length=50, required=True)
    city = forms.ChoiceField(choices=CITIES, required=True, widget=forms.Select)
    phone_number = forms.IntegerField(min_value=0, max_value=999999999, required=True)
    email = forms.EmailField(widget=forms.EmailInput, required=True)
    emergency_contact_name = forms.CharField(max_length=60, required=True)
    emergency_contact_phone_number = forms.IntegerField(min_value=0, max_value=999999999, required=True)


class EditMemberProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1922, 2022), attrs={'class': 'form-control'}), required=True)
    building_number = forms.IntegerField(min_value=0, max_value=99999,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
    apartment_number = forms.IntegerField(min_value=0, max_value=99999, required=True,
                                          widget=forms.NumberInput(attrs={'class': 'form-control'}))
    street_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.ChoiceField(choices=CITIES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.IntegerField(min_value=0, max_value=999999999, required=True,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)

    emergency_contact_name = forms.CharField(max_length=60, required=True,
                                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    emergency_contact_phone_number = forms.IntegerField(min_value=0, max_value=999999999, required=True,
                                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ChangeMembershipNumberForm(forms.Form):
    member = forms.ChoiceField(label="Select Member", widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ChangeMembershipNumberForm, self).__init__(*args, **kwargs)
        self.fields['member'].choices = get_all_members()


class RegisterMemberVisitSelectForm(forms.Form):
    member = forms.ChoiceField(
        widget=forms.Select(
            attrs={"placeholder": "Select Member",'class': 'form-control'}), label="Select member", required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterMemberVisitSelectForm, self).__init__(*args, **kwargs)
        self.fields['member'].choices = get_all_members()


def get_event_hosts():
    hosts = []
    for host in EventHosts.objects.all():
        hosts.append((host.id, (host.first_name + host.last_name)))
    return hosts


class CreateEventForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
    event_host = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    event_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control'}))
    event_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    maximum_people = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.fields['event_host'].choices = get_event_hosts()

# def get_all_events():
#     events = []
#     for event in Events.objects.all():
#         events.append((event.id, (event.name + event.date)))
#     return events
#
#
# class RegisterForEventForm(forms.Form):
#     date = forms.DateField(widget=forms.SelectDateWidget)
#     event_host = forms.ChoiceField(widget=forms.Select)
#     event_name = forms.CharField(max_length=20)
#     event_description = forms.CharField(widget=forms.TextInput)
#     maximum_people = forms.IntegerField()
#
#     def __init__(self, *args, **kwargs):
#         super(CreateEventForm, self).__init__(*args, **kwargs)
#         self.fields['event_host'].choices = get_event_hosts()
