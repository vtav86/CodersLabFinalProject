from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from gym_app.forms import LoginForm, RegisterNewMemberForm, OnlineRegistrationForm, ManagePaymentForm, get_all_members, \
    ChangePasswordForm, EditProfileForm, EditMemberProfileForm, ChangeMembershipNumberForm, \
    RegisterMemberVisitSelectForm, CreateEventForm

#
# class BaseView(View):
#     def get(self, request):
#         return render(request, 'gym_app/base.html')
from gym_app.models import Members, MemberNumber, Payments, Visits, Events


class HomePageView(View):

    def get(self, request):
        if request.user.is_staff:
            return render(request, "gym_app/home.html", {'admin': 'admin'})
        else:
            return render(request, "gym_app/home.html")


class LoginView(View):

    def get(self, request):
        user = request.user
        auth = user.is_authenticated
        # if not logged in
        if auth is False:
            form = LoginForm()
            return render(request, 'gym_app/login.html', {'form': form})
        else:
            logged_in_statement = f'You are already logged in'
            return render(request, 'gym_app/login.html', {'already_logged_in': logged_in_statement})

    def post(self, request):
        user = request.user
        auth = user.is_authenticated
        # if not logged in
        if auth is False:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("login")
                else:
                    error_statement = "Incorrect username or password"
                    return render(request, 'gym_app/login.html',
                                  {'form': form, 'form_error': error_statement})
        else:
            logged_in_statement = f'{user} is already logged in'
            return render(request, 'gym_app/login.html', {'already_logged_in': logged_in_statement, 'admin': 'admin'})


class LogoutView(View):
    def get(self, request):
        user = request.user
        auth = user.is_authenticated
        if auth is not False:
            return render(request, "gym_app/logout.html", {'user': user, 'auth': auth})
        else:
            return render(request, "gym_app/logout.html")

    def post(self, request):
        logout(request)
        return render(request, "gym_app/logout.html")


class RegisterNewMemberView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff == True

    def handle_no_permission(self):
        return redirect("accessdenied")

    def get(self, request):
        form = RegisterNewMemberForm()
        return render(request, 'gym_app/register_new_member.html', {'form': form, 'admin': 'admin'})

    def post(self, request):
        form = RegisterNewMemberForm(request.POST)
        if form.is_valid():
            member_number = form.cleaned_data["member_number"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            building_number = form.cleaned_data["building_number"]
            apartment_number = form.cleaned_data["apartment_number"]
            street_name = form.cleaned_data["street_name"]
            city = form.cleaned_data["city"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            emergency_contact_name = form.cleaned_data["emergency_contact_name"]
            emergency_contact_phone_number = form.cleaned_data["emergency_contact_phone_number"]
            credentials = {'first_name': first_name,
                           'last_name': last_name,
                           'date_of_birth': date_of_birth,
                           'building_number': building_number,
                           'apartment_number': apartment_number,
                           'street_name': street_name,
                           'city': city,
                           'phone_number': phone_number,
                           'email': email,
                           'emergency_contact_name': emergency_contact_name,
                           'emergency_contact_phone_number': emergency_contact_phone_number,
                           }
            if request.POST.get('bypass') is None:
                if Members.objects.filter(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth):
                    existing_members = Members.objects.filter(first_name=first_name, last_name=last_name,
                                                              date_of_birth=date_of_birth)
                    return render(request, 'gym_app/register_new_member.html',
                                  {'form': form, 'existing_members': existing_members, 'admin': 'admin'})
                new_member = Members.objects.create(**credentials)
                MemberNumber.objects.create(member_number=member_number, member_id=new_member.id, expiry=datetime.now())
                return render(request, 'gym_app/register_new_member.html',
                              {'form': form, 'member_added': 'member_added', 'admin': 'admin'})
            elif request.POST.get('bypass') is not None:
                new_member = Members.objects.create(**credentials)
                MemberNumber.objects.create(member_number=member_number, member_id=new_member.id, expiry=datetime.now())
                return render(request, 'gym_app/register_new_member.html',
                              {'form': form, 'member_add_bypass': 'member_add_bypass', 'admin': 'admin'})
        elif not form.is_valid():
            return render(request, 'gym_app/register_new_member.html', {'form': form, 'admin': 'admin'})


def check_member_number_last_name(member_number, last_name):
    member = MemberNumber.objects.get(member_number=member_number)
    print(member)
    member_verification = Members.objects.get(pk=member.member_id)
    print(member_verification.last_name)
    if member_verification.last_name == last_name:
        return True
    else:
        return False


class OnlineRegistrationView(View):
    def get(self, request):
        user = request.user
        auth = user.is_authenticated
        if auth is False:
            form = OnlineRegistrationForm()
            if request.user.is_staff:
                return render(request, "gym_app/online_registration.html", {'form': form, 'admin': 'admin'})
            else:
                return render(request, "gym_app/online_registration.html", {'form': form})
        else:
            if request.user.is_staff:
                return render(request, "gym_app/online_registration.html",
                              {'already_logged_in': 'logged_in_statement', 'admin': 'admin'})
            else:
                return render(request, "gym_app/online_registration.html",
                              {'already_logged_in': 'logged_in_statement'})

    def post(self, request):
        form = OnlineRegistrationForm(request.POST)
        if form.is_valid():
            member_number = form.cleaned_data["member_number"]
            last_name = form.cleaned_data["last_name"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            if check_member_number_last_name(member_number, last_name) and password1 == password2:
                member_number_model = MemberNumber.objects.get(member_number=member_number)
                member = Members.objects.get(pk=member_number_model.member_id)
                try:
                    if User.objects.get(username=member_number):
                        already_registered = 'There is already an account for this member'
                        return render(request, "gym_app/online_registration.html",
                                      {'already_registered': already_registered, 'form': form, 'admin': 'admin'})
                except ObjectDoesNotExist:
                    new_user = User.objects.create(username=member_number,
                                                   first_name=member.first_name,
                                                   last_name=member.last_name,
                                                   email=member.email,
                                                   is_superuser=False,
                                                   is_staff=False,
                                                   is_active=True,
                                                   password=password1)
                    new_user.set_password(password1)
                    new_user.save()
                    return render(request, 'gym_app/online_registration.html',
                                  {'form': form, 'admin': 'admin', 'registered': 'registered'})
            else:
                return render(request, 'gym_app/online_registration.html',
                              {'form': form, 'admin': 'admin', 'mismatch': 'mismatch'})
        else:
            return render(request, 'gym_app/online_registration.html', {'form': form, 'admin': 'admin'})


def check_for_errors():
    error_list = []
    for member in Members.objects.all():
        try:
            MemberNumber.objects.get(member_id=member.id)
        except ObjectDoesNotExist:
            error_list.append(
                (member.id, ('ID ' + str(member.id) + ' | Name ' + member.last_name + ', ' + member.first_name)))
    return error_list


PAYMENTTYPE = (
    ('Cash', 'Cash'),
    ('Card', 'Card'),
    ('Voucher', 'Voucher')
)

SUBSCRIPTIONS = (
    (30, '30 Days'),
    (90, '90 Days'),
    (180, '180 Days'),
    (365, '365 Days')
)


class ManagePaymentView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff == True

    def handle_no_permission(self):
        return redirect("accessdenied")

    def get(self, request):
        form = ManagePaymentForm()
        return render(request, "gym_app/manage_payment.html",
                      {'form': form, 'errors': check_for_errors(), 'admin': 'admin'})

    def post(self, request):
        form = ManagePaymentForm(request.POST)
        if form.is_valid():
            member = request.POST["member"]
            payment_history = Payments.objects.filter(member_id=member)
            expiry_date = MemberNumber.objects.filter(member_id=member)
            if request.POST.get("next"):
                return render(request, "gym_app/manage_payment.html",
                              {'form': form, 'confirmation': 'confirmation', 'payment_history': payment_history,
                               'expiry': expiry_date, 'payment_type': PAYMENTTYPE, 'subscription': SUBSCRIPTIONS,
                               'admin': 'admin'})
            if request.POST.get("payment_confirmation"):
                payment_type = request.POST["payment_type"]
                subscription = request.POST["subscription"]
                payment_amount = request.POST["payment_amount"]
                Payments.objects.create(member_id=member, payment_type=payment_type, payment_date=datetime.now(),
                                        subscription_period=subscription, payment_amount=payment_amount)
                member_object = MemberNumber.objects.get(member_id=member)
                current_expiry = MemberNumber.objects.get(member_id=member).expiry
                member_object.expiry = current_expiry + timedelta(days=int(subscription))
                member_object.save()

                return render(request, "gym_app/manage_payment.html",
                              {'form': form, 'new_expiry_date': member_object, 'member': member_object,
                               'admin': 'admin'})
        else:
            return render(request, "gym_app/manage_payment.html",
                          {'form': form, 'errors': check_for_errors(), 'admin': 'admin'})


class MyProfileView(View):
    def get(self, request):
        user = request.user
        auth = user.is_authenticated
        int_user = user.username
        if auth is False:
            return redirect("login")
        else:
            member_model_id = MemberNumber.objects.get(member_number=int_user).member_id
            member_details = Members.objects.get(id=member_model_id)
            print(self.request.user.is_staff)
            if self.request.user.is_staff:
                return render(request, 'gym_app/my_profile.html',
                              {'member_number': int_user, 'member_details': member_details,
                               'already_logged_in': 'already_logged_in', 'admin': 'admin'})
            else:
                return render(request, 'gym_app/my_profile.html',
                              {'member_number': int_user, 'member_details': member_details,
                               'already_logged_in': 'already_logged_in'})


class ChangePasswordView(View):
    def get(self, request):
        form = ChangePasswordForm()
        user = request.user
        auth = user.is_authenticated
        if auth is True:
            if self.request.user.is_staff == True:
                return render(request, "gym_app/change_password.html", {'form': form, 'user': user, 'admin': 'admin'})
            else:
                return render(request, "gym_app/change_password.html", {'form': form, 'user': user})
        else:
            return redirect("login")

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        user = request.user
        int_user = int(user.username)
        user_info = User.objects.get(username=int_user)
        if form.is_valid():
            current_password = form.cleaned_data["current_password"]
            authenticate_user = authenticate(username=user.username, password=current_password)
            if authenticate_user is None:
                incorrect_password = 'Current password not correct'
                return render(request, "gym_app/change_password.html",
                              {'form': form, 'user': user, 'incorrect_password': incorrect_password, 'admin': 'admin'})
            password1 = form.cleaned_data["password1"]
            user.set_password(password1)
            user.save()
            login(request, user)
            if self.request.user.is_staff == True:
                return render(request, "gym_app/change_password.html",
                              {'user': user, 'password_updated': 'password_updated', 'form': form, 'admin': 'admin'})
            else:
                return render(request, "gym_app/change_password.html",
                              {'user': user, 'password_updated': 'password_updated', 'form': form})

        else:
            return render(request, "gym_app/change_password.html", {'form': form, 'user': user, 'admin': 'admin'})


class EditMyProfileView(View):
    def get(self, request):
        logged_in_user = request.user
        auth = logged_in_user.is_authenticated
        if auth is True:
            user_number = MemberNumber.objects.get(member_number=logged_in_user.username)
            user = Members.objects.get(id=user_number.member_id)
            member_number = logged_in_user
            first_name = user.first_name
            last_name = user.last_name
            form = EditProfileForm(initial={
                'date_of_birth': user.date_of_birth,
                'building_number': user.building_number,
                'apartment_number': user.apartment_number,
                'street_name': user.street_name,
                'city': user.city,
                'phone_number': user.phone_number,
                'email': user.email,
                'emergency_contact_name': user.emergency_contact_name,
                'emergency_contact_phone_number': user.emergency_contact_phone_number
            })
            if self.request.user.is_staff == True:
                return render(request, "gym_app/edit_profile.html",
                              {'form': form, 'member_number': member_number, 'first_name': first_name,
                               'last_name': last_name, 'admin': 'admin'})
            else:
                return render(request, "gym_app/edit_profile.html",
                              {'form': form, 'member_number': member_number, 'first_name': first_name,
                               'last_name': last_name})
        else:
            return redirect("login")

    def post(self, request):
        logged_in_user = request.user
        form = EditProfileForm(request.POST)
        if form.is_valid():
            member_id = MemberNumber.objects.get(member_number=logged_in_user.username).member_id
            user = Members.objects.get(id=member_id)
            user.date_of_birth = form.cleaned_data["date_of_birth"]
            user.building_number = form.cleaned_data["building_number"]
            user.apartment_number = form.cleaned_data["apartment_number"]
            user.street_name = form.cleaned_data["street_name"]
            user.city = form.cleaned_data["city"]
            user.phone_number = form.cleaned_data["phone_number"]
            user.email = form.cleaned_data["email"]
            user.emergency_contact_name = form.cleaned_data["emergency_contact_name"]
            user.emergency_contact_phone_number = form.cleaned_data["emergency_contact_phone_number"]
            user.save()
            return render(request, "gym_app/edit_profile.html",
                          {'form': form, 'successful': 'successful', 'member_number': logged_in_user,
                           'first_name': user.first_name, 'admin': 'admin'})
        else:
            return render(request, "gym_app/edit_profile.html", {'form': form})


class ViewMembersView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff == True

    def handle_no_permission(self):
        return redirect("accessdenied")

    def get(self, request):
        logged_in_user = request.user
        auth = logged_in_user.is_authenticated
        all_member_numbers = MemberNumber.objects.all().order_by('member_number')
        date = datetime.now().date()
        return render(request, "gym_app/view_members.html",
                      {'all_member_numbers': all_member_numbers, 'date': date, 'admin': 'admin'})


class MemberPaymentView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff == True

    def handle_no_permission(self):
        return redirect("accessdenied")

    def get(self, request, id):
        member_details = MemberNumber.objects.get(member_id=id)
        payments = Payments.objects.filter(member_id=id)
        return render(request, "gym_app/member_payment.html",
                      {'member_details': member_details, 'payments': payments, 'payment_type': PAYMENTTYPE,
                       'subscription': SUBSCRIPTIONS, 'admin': 'admin'})

    def post(self, request, id):
        payment_type = request.POST["payment_type"]
        subscription = request.POST["subscription"]
        payment_amount = request.POST["payment_amount"]
        Payments.objects.create(member_id=id, payment_type=payment_type, payment_date=datetime.now(),
                                subscription_period=subscription, payment_amount=payment_amount)
        member_details = MemberNumber.objects.get(member_id=id)
        payments = Payments.objects.filter(member_id=id)
        current_expiry = member_details.expiry
        member_details.expiry = current_expiry + timedelta(days=int(subscription))
        member_details.save()

        return render(request, "gym_app/member_payment.html",
                      {'member_details': member_details, 'payments': payments, 'payment_type': PAYMENTTYPE,
                       'subscription': SUBSCRIPTIONS, 'admin': 'admin', 'payment_made': 'payment_made'})


class EditMemberProfileView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff == True

    def handle_no_permission(self):
        return redirect("accessdenied")

    def get(self, request, id):
        user = MemberNumber.objects.get(member_id=id)
        form = EditMemberProfileForm(initial={
            'first_name': user.member.first_name,
            'last_name': user.member.last_name,
            'date_of_birth': user.member.date_of_birth,
            'building_number': user.member.building_number,
            'apartment_number': user.member.apartment_number,
            'street_name': user.member.street_name,
            'city': user.member.city,
            'phone_number': user.member.phone_number,
            'email': user.member.email,
            'emergency_contact_name': user.member.emergency_contact_name,
            'emergency_contact_phone_number': user.member.emergency_contact_phone_number
        })
        return render(request, "gym_app/edit_member_profile.html", {'form': form, 'user': user, 'admin': 'admin'})

    def post(self, request, id):
        form = EditMemberProfileForm(request.POST)

        if form.is_valid():
            user = MemberNumber.objects.get(member_id=id)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.date_of_birth = form.cleaned_data["date_of_birth"]
            user.building_number = form.cleaned_data["building_number"]
            user.apartment_number = form.cleaned_data["apartment_number"]
            user.street_name = form.cleaned_data["street_name"]
            user.city = form.cleaned_data["city"]
            user.phone_number = form.cleaned_data["phone_number"]
            user.email = form.cleaned_data["email"]
            user.emergency_contact_name = form.cleaned_data["emergency_contact_name"]
            user.emergency_contact_phone_number = form.cleaned_data["emergency_contact_phone_number"]
            user.save()
            return render(request, "gym_app/edit_member_profile.html",
                          {'form': form, 'user': user, 'updated': 'updated', 'admin': 'admin'})
        else:
            return render(request, "gym_app/edit_member_profile.html",
                          {'form': form, 'admin': 'admin'})


class ChangeMembershipNumberView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff == True

    def handle_no_permission(self):
        return redirect("accessdenied")

    def get(self, request):
        form = ChangeMembershipNumberForm()
        return render(request, "gym_app/change_membership_number.html", {'form': form, 'admin': 'admin'})

    def post(self, request):
        form = ChangeMembershipNumberForm(request.POST)
        if request.POST.get("select"):
            return render(request, "gym_app/change_membership_number.html",
                          {'form': form, 'selected': 'selected', 'admin': 'admin'})

        elif request.POST.get("confirm_number"):
            new_number = request.POST["new_number"]

            if not MemberNumber.objects.filter(member_number=new_number):
                member_id = request.POST["member"]
                update_member_number = MemberNumber.objects.get(member_id=member_id)
                update_member_number.member_number = new_number
                update_member_number.save()
                form = ChangeMembershipNumberForm()
                return render(request, "gym_app/change_membership_number.html",
                              {'form': form, 'confirmed': 'confirmed', 'admin': 'admin'})
            else:
                return render(request, "gym_app/change_membership_number.html",
                              {'form': form, 'number_in_use': 'number_in_use', 'admin': 'admin'})


class RegisterMemberVisitView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff == True

    def handle_no_permission(self):
        return redirect("accessdenied")

    def get(self, request):
        form = RegisterMemberVisitSelectForm()
        return render(request, "gym_app/register_member_visit.html", {'form': form, 'admin': 'admin'})

    def post(self, request):
        form = RegisterMemberVisitSelectForm(request.POST)
        if not request.POST.get("manual_selection") and not request.POST.get("log_visit"):
            if form.is_valid():
                member = form.cleaned_data["member"]
                membership_number = MemberNumber.objects.get(member_id=member)
                print(membership_number)
                if membership_number.expiry > datetime.now().date():
                    Visits.objects.create(date=datetime.now().date(), time=datetime.now().time(),
                                          member_number_id=membership_number.id)
                    return render(request, "gym_app/register_member_visit.html",
                                  {'form': form, 'visit_logged': 'visit_logged', 'member_details': membership_number,
                                   'admin': 'admin'})
                else:
                    return render(request, "gym_app/register_member_visit.html",
                                  {'form': form, 'membership_expired': 'membership_expired',
                                   'member_details': membership_number, 'admin': 'admin'})
        if request.POST.get("manual_selection"):
            return render(request, "gym_app/register_member_visit.html",
                          {'form': form, 'manual_input': 'manual_input', 'admin': 'admin'})
        if request.POST.get("log_visit"):
            entered_member_number = request.POST["entered_member_number"]
            try:
                if MemberNumber.objects.get(member_number=entered_member_number):
                    membership_number = MemberNumber.objects.get(member_number=entered_member_number)
                    if membership_number.expiry > datetime.now().date():
                        Visits.objects.create(date=datetime.now().date(), time=datetime.now().time(),
                                              member_number_id=membership_number.id)
                        return render(request, "gym_app/register_member_visit.html",
                                      {'form': form, 'admin': 'admin', 'visit_logged': 'visit_logged'})
                    else:
                        return render(request, "gym_app/register_member_visit.html",
                                      {'form': form, 'membership_expired': 'membership_expired',
                                       'member_details': membership_number, 'admin': 'admin'})
            except ObjectDoesNotExist:
                return render(request, "gym_app/register_member_visit.html",
                              {'form': form, 'member_not_found': 'member_not_found', 'admin': 'admin'})


class CreateEventView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff == True

    def handle_no_permission(self):
        return redirect("accessdenied")

    def get(self, request):
        form = CreateEventForm()
        return render(request, "gym_app/create_event.html", {'form': form, 'admin': 'admin'})

    def post(self, request):
        form = CreateEventForm(request.POST)
        if form.is_valid():
            new_event = Events.objects.create(
                date=form.cleaned_data["date"],
                maximum_people=form.cleaned_data["maximum_people"],
                event_name=form.cleaned_data["event_name"],

                event_description=form.cleaned_data["event_description"]
            )
            new_event.event_host.set(form.cleaned_data["event_host"])
            return render(request, "gym_app/create_event.html",
                          {'form': form, 'new_event': new_event, 'admin': 'admin'})
        else:
            return render(request, "gym_app/create_event.html", {'form': form, 'admin': 'admin'})


def current_event_registrations():
    current_registrations = []
    for each in Events.objects.all():
        for _ in each.event_members.all():
            current_registrations.append(((_.id), (each.id)))
    return tuple(current_registrations)


def count_attendees(registrations, event_id):
    qty = 0
    for each in registrations:
        if each[0] == event_id:
            qty += 1

    return qty


def list_of_events_and_attendees():
    events = Events.objects.all()
    events2 = events.all()
    total_events = []
    complete = {}
    for each in events2:
        for _ in each.event_members.all():
            total_events.append(each.id)
    for each in total_events:
        complete[each] = total_events.count(each)

    return complete


class ViewAllEventsView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff == True

    def handle_no_permission(self):
        return redirect("accessdenied")

    def get(self, request):
        events = Events.objects.all()
        return render(request, "gym_app/view_all_events.html",
                      {'events': events, 'registered': list_of_events_and_attendees().items(), 'admin': 'admin'})


class ViewEventInfoView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff == True

    def handle_no_permission(self):
        return redirect("accessdenied")

    def get(self, request, id):
        event_info = Events.objects.get(pk=id)
        registered = event_info.event_members.all()
        form = CreateEventForm(initial={
            'date': event_info.date,
            'event_name': event_info.event_name,
            'event_description': event_info.event_description,
            'maximum_people': event_info.maximum_people
        })
        return render(request, "gym_app/view_event_info.html",
                      {'event_info': event_info, 'form': form, 'admin': 'admin', 'registered': registered})

    def post(self, request, id):
        form = CreateEventForm(request.POST)
        event_info = Events.objects.get(pk=id)
        registered = event_info.event_members.all()
        if form.is_valid():
            if request.POST.get("Save"):
                event_info = Events.objects.get(pk=id)
                event_info.event_name = form.cleaned_data["event_name"]
                event_info.event_description = form.cleaned_data["event_description"]
                event_info.event_date = form.cleaned_data["date"]
                event_info.maximum_people = form.cleaned_data["maximum_people"]
                event_info.event_host.set(form.cleaned_data["event_host"])
                event_info.save()
                return render(request, "gym_app/view_event_info.html",
                              {'event_info': event_info, 'form': form, 'updated': 'updated', 'admin': 'admin',
                               'registered': registered})
            elif request.POST.get("Delete"):
                return render(request, "gym_app/view_event_info.html",
                              {'form': form, 'delete_event': 'delete_event', 'admin': 'admin',
                               'registered': registered})
            elif request.POST.get("Confirm Delete"):
                event_info = Events.objects.get(pk=id)
                event_info.delete()
                return render(request, "gym_app/view_event_info.html",
                              {'deleted': 'deleted'})


class MyEventsView(View):
    def get(self, request):
        user = request.user
        auth = user.is_authenticated
        # if not logged in
        if auth is False:
            return redirect("login")
        else:
            member = MemberNumber.objects.get(member_number=user.username)
            events = Events.objects.all()
            registered_events = Events.objects.filter(event_members=member.id)
            if request.user.is_staff:
                return render(request, "gym_app/my_events.html",
                              {'events': events, 'registered_events': registered_events, 'admin': 'admin'})
            else:
                return render(request, "gym_app/my_events.html",
                              {'events': events, 'registered_events': registered_events})


class RegisterForEventView(View):
    def get(self, request, event_id):
        user = request.user
        auth = user.is_authenticated
        # if not logged in
        if auth is False:
            return redirect("login")
        else:
            event = Events.objects.get(pk=event_id)
            reg = []
            for each in Events.objects.filter(id=event_id):
                for _ in each.event_members.all():
                    reg.append(_.id)
            if not event.event_members.filter(member_number=user.username):
                return render(request, "gym_app/view_event.html",
                              {'event': event, 'number_registered': len(reg), 'admin': 'admin'})
            else:
                return render(request, "gym_app/view_event.html",
                              {'event': event, 'number_registered': len(reg), 'admin': 'admin',
                               'registered': 'registered'})

    def post(self, request, event_id):
        user = request.user
        auth = user.is_authenticated
        reg = []
        for each in Events.objects.filter(id=event_id):
            for _ in each.event_members.all():
                reg.append(_.id)
        if auth is False:
            return redirect("login")

        if request.POST.get("cancel"):
            member_number_object = MemberNumber.objects.get(member_number=user.username)
            event = Events.objects.get(pk=event_id)
            event.event_members.remove(member_number_object.id)
            return render(request, "gym_app/view_event.html",
                          {'event': event, 'number_registered': len(reg), 'cancel': 'cancel'})
        else:
            member_number_object = MemberNumber.objects.get(member_number=user.username)
            event = Events.objects.get(pk=event_id)
            if not event.event_members.filter(member_number=user.username):
                event.event_members.add(member_number_object.id)
                return render(request, "gym_app/view_event.html",
                              {'event': event, 'number_registered': len(reg), 'nowregistered': 'nowregistered'})
            else:
                return render(request, "gym_app/view_event.html",
                              {'event': event, 'number_registered': len(reg), 'admin': 'admin',
                               'registered': 'registered'})


class AccessDeniedView(View):
    def get(self, request):
        return render(request, "gym_app/access_denied.html", {'admin': 'admin'})
