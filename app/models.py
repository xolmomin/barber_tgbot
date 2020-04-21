from django.db import models


class TgUser(models.Model):
    user_id = models.IntegerField(unique=True)
    step = models.IntegerField(default=0)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=32, null=True, blank=True)
    latitude = models.CharField(max_length=32, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    check = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_id}'


class Barber(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.user_id}'


class NearBarber(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE, null=True)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, null=True)
    length = models.FloatField(null=True, blank=True)
    sort_by_leng = models.IntegerField(null=True, blank=True)
