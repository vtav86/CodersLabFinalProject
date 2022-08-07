from django.db import models


class Members(models.Model):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    date_of_birth = models.DateField(null=False)
    building_number = models.IntegerField()
    apartment_number = models.IntegerField(null=False)
    street_name = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=40, null=False)
    phone_number = models.IntegerField(null=False)
    email = models.EmailField(null=False)
    emergency_contact_name = models.CharField(max_length=60, null=False)
    emergency_contact_phone_number = models.IntegerField(null=False)



    class Meta:
        verbose_name_plural = 'Members'

    def __str__(self):
        return self.last_name, self.first_name


class MemberNumber(models.Model):
    member_number = models.IntegerField(unique=True)
    member = models.OneToOneField(Members, on_delete=models.CASCADE)
    expiry = models.DateField(null=True)

    def __str__(self):
        info = f'Member Number {self.member_number} | {self.member.first_name}  {self.member.last_name}'
        return info


class Payments(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE, null=False)
    payment_type = models.CharField(max_length=20, null=False)
    payment_date = models.DateField(auto_now_add=True)
    subscription_period = models.CharField(max_length=20, null=False)
    payment_amount = models.IntegerField(null=False)


class Visits(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    member_number = models.ForeignKey(MemberNumber, on_delete=models.CASCADE)

    def __str__(self):
        info = f'Member Number {self.member_number} | {self.date}'
        return info

    class Meta:
        verbose_name_plural = 'Visits'

class EventHosts(models.Model):
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    phone_number = models.IntegerField(null=False)
    email = models.EmailField(null=False)



class Events(models.Model):
    date = models.DateField(null=False)
    maximum_people = models.IntegerField(null=False)
    event_name= models.CharField(max_length=20, null=False)
    event_description = models.TextField(null=False)
    event_host = models.ManyToManyField(EventHosts)
    event_members = models.ManyToManyField(MemberNumber)
