from django.contrib import admin

from gym_app.models import Members, MemberNumber, Payments, Visits, Events, EventHosts

admin.site.register(Members)
admin.site.register(MemberNumber)
admin.site.register(Payments)
admin.site.register(Visits)
admin.site.register(Events)
admin.site.register(EventHosts)
