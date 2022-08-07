from django.contrib import admin

from gym_app.models import Members, MemberNumber, Payments, Visits

admin.site.register(Members)
admin.site.register(MemberNumber)
admin.site.register(Payments)
admin.site.register(Visits)

