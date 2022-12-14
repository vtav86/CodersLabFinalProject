from datetime import date, time
from django.contrib.auth.models import User
import pytest
from gym_app.models import Members, MemberNumber, Visits, Payments, Events


def test_home_page_view_access(client):
    """Check that the home page is accessible"""
    response = client.get("/")
    assert response.status_code == 200


def test_about_page_view_access(client):
    """Check that the about page is accessible"""
    response = client.get("/about/")
    assert response.status_code == 200


def test_pricing_page_view_access(client):
    """Check that the pricing page is accessible"""
    response = client.get("/pricing/")
    assert response.status_code == 200


def test_contact_page_view_access(client):
    """Check that the contact page is accessible"""
    response = client.get("/contact/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_member_page_view_access(client):
    """Check that the member registration page is accessible"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/register-member/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_visit_view_access(client):
    """Check that the visit log page is accessible with staff login"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/register-member-visit/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_manage_payment_view_access(client):
    """Check that the payment management page is accessible with staff log in"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/manage-payment/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_event_view_access(client):
    """Check that the event creation page is accessible with staff log in"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/create-event/")
    assert response.status_code == 200


#
@pytest.mark.django_db
def test_all_members_view_access(client):
    """Check that the page to view all members is accessible with staff log in"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/view-members/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_change_membership_number_view_access(client):
    """Check that the payment to update member numbers is accessible with staff log in"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/change-membership-number/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_should_verify_member_add(client, create_member):
    """Test creates a new member and member number, and checks details correct against test model"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/register-member/")
    assert response.status_code == 200
    member = Members.objects.get(first_name="John")
    member_number = MemberNumber.objects.get(member_id=member.id)
    assert member.first_name == "John"
    assert member.last_name == "Smith"
    assert member.phone_number == 123123
    assert member_number.member_number == 9876
    assert member_number.id == 1
    assert member_number.member_number == 9876


@pytest.mark.django_db
def test_should_register_visit(client, create_member, register_visit):
    """Test registers a visit and checks details correct against test model"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/register-member-visit/")
    assert response.status_code == 200
    visit = Visits.objects.get(
        member_number=MemberNumber.objects.get(member_number=9876)
    )
    assert visit.date == date(2022, 8, 9)
    assert visit.time == time(3, 30, 00)


@pytest.mark.django_db
def test_should_manage_payment(client, create_member, register_visit, manage_payment):
    """Test creates a member and registers payments"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/manage-payment/")
    assert response.status_code == 200
    member_instance = Members.objects.get(first_name="John")
    payment = Payments.objects.get(member=member_instance)
    assert payment.payment_type == "Cash"
    assert payment.payment_date == date(2022, 8, 9)
    assert payment.payment_amount == 1000
    assert payment.subscription_period == "30"


@pytest.mark.django_db
def test_should_create_event(client, create_member, create_event):
    """Test creates a member and an event and checks details correct against test model"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/create-event/")
    assert response.status_code == 200
    event = Events.objects.get(event_name="Test Event")
    assert event.event_description == "A Trial Run"
    assert event.date == date(2023, 8, 19)
    host = event.event_host.get(pk=1)
    assert host.first_name == "Sean"


@pytest.mark.django_db
def test_should_delete_event(client, create_member, create_event, delete_event):
    """Test creates then deletes an event, confirms that no events exist afterwards"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/create-event/")
    assert response.status_code == 200
    event = Events.objects.all()
    assert len(event) == 0


@pytest.mark.django_db
def test_should_view_all_events(client, create_member, multiple_events):
    """Test creates members and assigns them to multiple events."""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/view-all-events/")
    assert response.status_code == 200
    context_events = response.context["events"]
    assert list(context_events) == list(multiple_events)


@pytest.mark.django_db
def test_should_view_all_members(client, create_multiple_members):
    """Test creates multiple members and checks they are returned in the view context"""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/view-members/")
    assert response.status_code == 200
    context_members = response.context["all_member_numbers"]
    assert list(context_members) == list(create_multiple_members)


@pytest.mark.django_db
def test_should_change_membership_number(
        client, create_member, change_membership_number
):
    """Test creates new member and updates membership to verify."""
    user = User.objects.create(username="user", is_superuser=True, is_staff=True)
    client.force_login(user)
    response = client.get("/change-membership-number/")
    assert response.status_code == 200
    member_number_instance = MemberNumber.objects.get(member_number=9877)
    assert member_number_instance.member_number == 9877
