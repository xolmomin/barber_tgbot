from django.contrib import admin

from app.models import TgUser, NearBarber, Barber

admin.site.register(TgUser)
admin.site.register(Barber)
admin.site.register(NearBarber)
