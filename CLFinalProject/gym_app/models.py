from django.db import models


class Members(models.Model):
    """Member instances created in this model. Required to create member numbers"""

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
        verbose_name_plural = "Members"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class MemberNumber(models.Model):
    """Member Numbers assigned to instances of members. Member Numbers must be unique"""

    member_number = models.IntegerField(unique=True)
    member = models.OneToOneField(Members, on_delete=models.CASCADE)
    expiry = models.DateField(null=True)

    def __str__(self):
        info = f"Member Number {self.member_number} | {self.member.first_name}  {self.member.last_name}"
        return info


class Payments(models.Model):
    """Payments registered in this class in order to maintain member subscription expiry"""

    member = models.ForeignKey(Members, on_delete=models.CASCADE, null=False)
    payment_type = models.CharField(max_length=20, null=False)
    payment_date = models.DateField(auto_now_add=True)
    subscription_period = models.CharField(max_length=20, null=False)
    payment_amount = models.IntegerField(null=False)

    class Meta:
        verbose_name_plural = "Payments"

    def __str__(self):
        return (
            f"{self.member.first_name} {self.member.last_name} | {self.payment_date} "
        )


class Visits(models.Model):
    """Occurances of member visitations is logged here"""

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    member_number = models.ForeignKey(MemberNumber, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Visits"

    def __str__(self):
        info = f"{self.member_number} | {self.date}"
        return info


class EventHosts(models.Model):
    """Registration of new hosts for events"""

    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    phone_number = models.IntegerField(null=False)
    email = models.EmailField(null=False)

    class Meta:
        verbose_name_plural = "Event Hosts"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Events(models.Model):
    """Create events where members can register to attend"""

    date = models.DateField(null=False)
    maximum_people = models.IntegerField(null=False)
    event_name = models.CharField(max_length=20, null=False)
    event_description = models.TextField(null=False)
    event_host = models.ManyToManyField(EventHosts)
    event_members = models.ManyToManyField(MemberNumber)

    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.event_name} {self.date}"
