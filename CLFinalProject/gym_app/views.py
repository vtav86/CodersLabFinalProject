from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
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
from gym_app.models import Members, MemberNumber, Payments, Visits


class HomePageView(View):
    def get(self, request):
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
                    return render(request, 'gym_app/login.html', {'form': form, 'form_error': error_statement})
        else:
            logged_in_statement = f'{user} is already logged in'
            return render(request, 'gym_app/login.html', {'already_logged_in': logged_in_statement})


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


class RegisterNewMemberView(View):
    def get(self, request):
        form = RegisterNewMemberForm()
        return render(request, 'gym_app/register_new_member.html', {'form': form})

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
                                  {'form': form, 'existing_members': existing_members})
                new_member = Members.objects.create(**credentials)
                MemberNumber.objects.create(member_number=member_number, member_id=new_member.id, expiry=datetime.now())
                return HttpResponse(f'{new_member.first_name} with {member_number} added!')
            elif request.POST.get('bypass') is not None:
                new_member = Members.objects.create(**credentials)
                MemberNumber.objects.create(member_number=member_number, member_id=new_member.id, expiry=datetime.now())
                return HttpResponse(f'{new_member.first_name} with {member_number} added after bypass clicked!')
        elif not form.is_valid():
            return render(request, 'gym_app/register_new_member.html', {'form': form})


def check_member_number_last_name(member_number, last_name):
    member = MemberNumber.objects.get(member_number=member_number)
    member_verification = Members.objects.get(pk=member.member_id)
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
            return render(request, "gym_app/online_registration.html", {'form': form})
        else:
            logged_in_statement = f'Looks like you are already logged in! Logout to register for online access.'
            return render(request, "gym_app/online_registration.html", {'already_logged_in': logged_in_statement})

    def post(self, request):
        form = OnlineRegistrationForm(request.POST)
        if form.is_valid():
            member_number = form.cleaned_data["member_number"]
            last_name = form.cleaned_data["last_name"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            if check_member_number_last_name(member_number, last_name) and password1 == password2:
                # retrieve information
                member_number_model = MemberNumber.objects.get(member_number=member_number)
                member = Members.objects.get(pk=member_number_model.member_id)
                if MemberNumber.objects.get(member_number=member_number, member_id=member_number_model.member_id):
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
                elif not MemberNumber.objects.get(member_number=member_number, member_id=member_number_model.member_id):
                    already_registered = 'There is already an account for this member'
                    return render(request, "gym_app/online_registration.html",
                                  {'already_registered': already_registered, 'form': form})

                return HttpResponse('You are now registered for online access')


        elif not form.is_valid():
            return render(request, 'gym_app/online_registration.html', {'form': form})


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


class ManagePaymentView(View):
    def get(self, request):
        form = ManagePaymentForm()
        return render(request, "gym_app/manage_payment.html", {'form': form, 'errors': check_for_errors()})

    def post(self, request):
        form = ManagePaymentForm(request.POST)
        if form.is_valid():
            member = request.POST["member"]
            payment_history = Payments.objects.filter(member_id=member)
            expiry_date = MemberNumber.objects.filter(member_id=member)
            if request.POST.get("next"):
                return render(request, "gym_app/manage_payment.html",
                              {'form': form, 'confirmation': 'confirmation', 'payment_history': payment_history,
                               'expiry': expiry_date, 'payment_type': PAYMENTTYPE, 'subscription': SUBSCRIPTIONS})
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
                              {'form': form, 'new_expiry_date': member_object, 'member': member_object})
        else:
            return render(request, "gym_app/manage_payment.html", {'form': form, 'errors': check_for_errors()})


class MyProfileView(View):
    def get(self, request):
        user = request.user
        auth = user.is_authenticated
        int_user = user.username
        if auth is False:
            form = LoginForm()
            return redirect("login")
        else:
            member_model_id = MemberNumber.objects.get(member_number=int_user).member_id
            member_details = Members.objects.get(id=member_model_id)
            return render(request, 'gym_app/my_profile.html',
                          {'member_number': int_user, 'member_details': member_details,
                           'already_logged_in': 'already_logged_in'})


class ChangePasswordView(View):
    def get(self, request):
        form = ChangePasswordForm()
        user = request.user
        auth = user.is_authenticated
        if auth is True:
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
                              {'form': form, 'user': user, 'incorrect_password': incorrect_password})
            password1 = form.cleaned_data["password1"]
            user.set_password(password1)
            user.save()
            login(request, user)
            return render(request, "gym_app/change_password.html",
                          {'user': user, 'password_updated': 'password_updated', 'form': form})
        else:
            return render(request, "gym_app/change_password.html", {'form': form, 'user': user})


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
                           'first_name': user.first_name})
        else:
            return render(request, "gym_app/edit_profile.html", {'form': form})


class ViewMembersView(View):
    def get(self, request):
        logged_in_user = request.user
        auth = logged_in_user.is_authenticated
        all_member_numbers = MemberNumber.objects.all().order_by('member_number')
        date = datetime.now().date()
        return render(request, "gym_app/view_members.html",
                      {'all_member_numbers': all_member_numbers, 'date': date})


class MemberPaymentView(View):
    def get(self, request, id):
        member_details = MemberNumber.objects.get(member_id=id)
        payments = Payments.objects.filter(member_id=id)
        return render(request, "gym_app/member_payment.html",
                      {'member_details': member_details, 'payments': payments, 'payment_type': PAYMENTTYPE,
                       'subscription': SUBSCRIPTIONS})

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
                       'subscription': SUBSCRIPTIONS})


class EditMemberProfileView(View):
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
        return render(request, "gym_app/edit_member_profile.html", {'form': form, 'user': user})

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
                          {'form': form, 'user': user, 'updated': 'updated'})
        else:
            return render(request, "gym_app/edit_member_profile.html",
                          {'form': form})


class ChangeMembershipNumberView(View):
    def get(self, request):
        form = ChangeMembershipNumberForm()
        return render(request, "gym_app/change_membership_number.html", {'form': form})

    def post(self, request):
        form = ChangeMembershipNumberForm(request.POST)
        if request.POST.get("select"):
            return render(request, "gym_app/change_membership_number.html", {'form': form, 'selected': 'selected'})

        elif request.POST.get("confirm_number"):
            new_number = request.POST["new_number"]

            if not MemberNumber.objects.filter(member_number=new_number):
                member_id = request.POST["member"]
                update_member_number = MemberNumber.objects.get(member_id=member_id)
                update_member_number.member_number = new_number
                update_member_number.save()
                form = ChangeMembershipNumberForm()
                return render(request, "gym_app/change_membership_number.html",
                              {'form': form, 'confirmed': 'confirmed'})
            else:
                return render(request, "gym_app/change_membership_number.html",
                              {'form': form, 'number_in_use': 'number_in_use'})


class RegisterMemberVisitView(View):
    def get(self, request):
        form = RegisterMemberVisitSelectForm()
        return render(request, "gym_app/register_member_visit.html", {'form': form})

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
                                  {'form': form, 'visit_logged': 'visit_logged', 'member_details': membership_number})
                else:
                    return render(request, "gym_app/register_member_visit.html",
                                  {'form': form, 'membership_expired': 'membership_expired',
                                   'member_details': membership_number})
        if request.POST.get("manual_selection"):
            # entered_member_number = request.POST["entered_member_number "]
            return render(request, "gym_app/register_member_visit.html", {'form': form, 'manual_input': 'manual_input'})
        if request.POST.get("log_visit"):
            entered_member_number = request.POST["entered_member_number"]
            try:
                if MemberNumber.objects.get(member_number=entered_member_number):
                    membership_number = MemberNumber.objects.get(member_number=entered_member_number)
                    if membership_number.expiry > datetime.now().date():
                        Visits.objects.create(date=datetime.now().date(), time=datetime.now().time(),
                                              member_number_id=membership_number.id)
                        return render(request, "gym_app/register_member_visit.html", {'form': form})
                    else:
                        return render(request, "gym_app/register_member_visit.html",
                                      {'form': form, 'membership_expired': 'membership_expired',
                                       'member_details': membership_number})
            except ObjectDoesNotExist:
                return render(request, "gym_app/register_member_visit.html",
                              {'form': form, 'member_not_found': 'member_not_found'})

class CreateEventView(View):
    def get(self, request):
        form = CreateEventForm()
        return render(request, "gym_app/create_event.html", {'form': form})
