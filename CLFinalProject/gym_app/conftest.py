import pytest as pytest
from django.test import Client
from datetime import date, datetime
from gym_app.models import Members, MemberNumber, Visits, Payments, EventHosts, Events


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def create_member():
    new_member = Members.objects.create(
        id=1,
        first_name="John",
        last_name="Smith",
        date_of_birth=date(1990, 1, 1),
        building_number=1,
        apartment_number=2,
        street_name="Avet",
        city="Yerevan",
        phone_number=123123,
        email="test@test.com",
        emergency_contact_name="Joe",
        emergency_contact_phone_number=2331233
    )
    member_number = MemberNumber.objects.create(member_number=9876, member_id=new_member.id, expiry=datetime.now())
    return member_number, new_member


@pytest.fixture
def register_visit():
    member_number_instance = MemberNumber.objects.get(member_number=9876)
    visit_instance = Visits.objects.create(
        member_number=member_number_instance)
    visit_instance.date = "2022-08-09"
    visit_instance.time = "03:30:00"
    visit_instance.save()
    return visit_instance


@pytest.fixture
def manage_payment():
    member_instance = Members.objects.get(first_name="John")
    payment = Payments.objects.create(
        member=member_instance,
        payment_type="Cash",
        subscription_period=30,
        payment_amount=1000)
    payment.payment_date = "2022-08-09"
    payment.save()
    return payment


@pytest.fixture
def create_event():
    member_instance = MemberNumber.objects.filter(pk=1)
    EventHosts.objects.create(
        first_name="Sean",
        last_name="Sampson",
        phone_number=5556666,
        email="sean@sampson.com")
    hosts = EventHosts.objects.filter(pk=1)
    event = Events()
    event.id = 1
    event.date = "2023-08-19"
    event.event_name = "Test Event"
    event.event_description = "A Trial Run"
    event.maximum_people = 10
    event.event_members.set(member_instance)
    event.save()
    event.event_host.set(hosts)
    event.save()
    return event


@pytest.fixture
def multiple_events():
    member_instance = MemberNumber.objects.filter(pk=1)
    EventHosts.objects.create(
        first_name="Sean",
        last_name="Sampson",
        phone_number=5556666,
        email="sean@sampson.com")
    hosts = EventHosts.objects.filter(pk=1)
    event1 = Events()
    event1.id = 1
    event1.date = "2023-08-19"
    event1.event_name = "First Test Event"
    event1.event_description = "A Trial Run"
    event1.maximum_people = 10
    event1.event_members.set(member_instance)
    event1.save()
    event1.event_host.set(hosts)
    event1.save()
    event2 = Events()
    event2.id = 2
    event2.date = "2023-08-19"
    event2.event_name = "Second Test Event"
    event2.event_description = "A Trial Run"
    event2.maximum_people = 10
    event2.event_members.set(member_instance)
    event2.save()
    event2.event_host.set(hosts)
    event2.save()
    event3 = Events()
    event3.id = 3
    event3.date = "2023-08-19"
    event3.event_name = "Third Test Event"
    event3.event_description = "A Trial Run"
    event3.maximum_people = 10
    event3.event_members.set(member_instance)
    event3.save()
    event3.event_host.set(hosts)
    event3.save()
    return event1, event2, event3


@pytest.fixture
def create_multiple_members():
    new_member1 = Members.objects.create(
        id=1,
        first_name="John",
        last_name="Smith",
        date_of_birth=date(1990, 1, 1),
        building_number=1,
        apartment_number=2,
        street_name="Avet",
        city="Yerevan",
        phone_number=123123,
        email="test@test.com",
        emergency_contact_name="Joe",
        emergency_contact_phone_number=2331233
    )
    member_number1 = MemberNumber.objects.create(member_number=9874, member_id=new_member1.id, expiry=datetime.now())
    new_member2 = Members.objects.create(
        id=2,
        first_name="Tom",
        last_name="Jones",
        date_of_birth=date(1990, 1, 1),
        building_number=1,
        apartment_number=2,
        street_name="Avet",
        city="Yerevan",
        phone_number=123123,
        email="test@test.com",
        emergency_contact_name="Joe",
        emergency_contact_phone_number=2331233
    )
    member_number2 = MemberNumber.objects.create(member_number=9875, member_id=new_member2.id, expiry=datetime.now())

    new_member3 = Members.objects.create(
        id=3,
        first_name="Lisa",
        last_name="Pratts",
        date_of_birth=date(1990, 1, 1),
        building_number=1,
        apartment_number=2,
        street_name="Avet",
        city="Yerevan",
        phone_number=123123,
        email="test@test.com",
        emergency_contact_name="Joe",
        emergency_contact_phone_number=2331233
    )
    member_number3 = MemberNumber.objects.create(member_number=9876, member_id=new_member3.id, expiry=datetime.now())

    return member_number1, member_number2, member_number3,

@pytest.fixture
def change_membership_number():
    member_number_instance = MemberNumber.objects.get(member_number=9876)
    member_number_instance.member_number = 9877
    member_number_instance.save()
    return member_number_instance

@pytest.fixture
def delete_event():
    event = Events.objects.get(pk=1)
    return event.delete()
