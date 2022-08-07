# {first_name: first_name,
#  last_name: last_name,
#  date_of_birth: date_of_birth,
#  building_number: building_number,
#  apartment_number: apartment_number,
#  street_name: street_name,
#  city: city,
#  phone_number: phone_number,
#  email: email,
#  emergency_contact_name: emergency_contact_name,
#  emergency_contact_phone_number: emergency_contact_phone_number}


# member_number = form.cleaned_data["member_number"]
# first_name = form.cleaned_data["first_name"]
# last_name = form.cleaned_data["last_name"]
# date_of_birth = form.cleaned_data["date_of_birth"]
# building_number = form.cleaned_data["building_number"]
# apartment_number = form.cleaned_data["apartment_number"]
# street_name = form.cleaned_data["street_name"]
# city = form.cleaned_data["city"]
# phone_number = form.cleaned_data["phone_number"]
# email = form.cleaned_data["email"]
# emergency_contact_name = form.cleaned_data["emergency_contact_name"]
# emergency_contact_phone_number = form.cleaned_data["emergency_contact_phone_number"]
# new_member = Members.objects.create(first_name=first_name,
#                                     last_name=last_name,
#                                     date_of_birth=date_of_birth,
#                                     building_number=building_number,
#                                     apartment_number=apartment_number,
#                                     street_name=street_name,
#                                     city=city,
#                                     phone_number=phone_number,
#                                     email=email,
#                                     emergency_contact_name=emergency_contact_name,
#                                     emergency_contact_phone_number=emergency_contact_phone_number)
# MemberNumber.objects.create(member_number=member_number, member_id=new_member.id)
# return HttpResponse(f'{new_member.first_name} with {member_number} added after bypass!')


# new_member = Members.objects.create(first_name=first_name,
#                                     last_name=last_name,
#                                     date_of_birth=date_of_birth,
#                                     building_number=building_number,
#                                     apartment_number=apartment_number,
#                                     street_name=street_name,
#                                     city=city,
#                                     phone_number=phone_number,
#                                     email=email,
#                                     emergency_contact_name=emergency_contact_name,
#                                     emergency_contact_phone_number=emergency_contact_phone_number)
# from gym_app.models import MemberNumber, Members
#
#
# def get_all_members():
#     choices = []
#     for member in MemberNumber.objects.all():
#         choices.append(member.id)
#     return choices
#
#
# # get_all_members()
# members = Members.objects.all()
# print(members)