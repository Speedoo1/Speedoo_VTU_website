import uuid

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils.timezone import now


class profile(AbstractUser):
    gend = (('Male', 'Male'), ('Female', 'Female'))
    username = models.CharField(unique=True, max_length=200)
    wallet = models.FloatField(default=0.0)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=20, default='+234')
    gender = models.CharField(max_length=20, choices=gend, default="male")
    pending_wallet = models.FloatField(default=0.0)
    display = models.FloatField(default=0.0)
    credit = models.FloatField(default=0.0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)


class waecprice(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200, default="")
    price = models.FloatField()

    def __str__(self):
        return str(self.name)


class datanetwork(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class airteldataplan(models.Model):
    value = models.CharField(max_length=200)
    datagb = models.CharField(max_length=200)
    dataprice = models.CharField(max_length=200)

    def __str__(self):
        return str(self.datagb)


class mobile9dataplan(models.Model):
    value = models.CharField(max_length=200)
    datagb = models.CharField(max_length=200)
    dataprice = models.CharField(max_length=200)

    def __str__(self):
        return str(self.datagb)


class glodataplan(models.Model):
    value = models.CharField(max_length=200)
    datagb = models.CharField(max_length=200)
    dataprice = models.CharField(max_length=200)

    def __str__(self):
        return str(self.datagb)


class mtndataplan(models.Model):
    value = models.CharField(max_length=200)
    datagb = models.CharField(max_length=200)
    dataprice = models.CharField(max_length=200)
    network = models.CharField(max_length=200, default='MTN')

    def __str__(self):
        return str(self.datagb)


class historydata(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    users = models.ForeignKey(profile, on_delete=models.CASCADE, )

    orderid = models.CharField(max_length=200, )
    statuscode = models.CharField(max_length=200)
    transaction_type = models.CharField(max_length=200, blank=True)
    amount = models.CharField(max_length=200, blank=True)
    product = models.CharField(max_length=1000, null=True, blank=True, default='')
    meternumber = models.CharField(max_length=1000, null=True, blank=True, default='')
    metertype = models.CharField(max_length=1000, null=True, blank=True, default='')
    phonenumber = models.CharField(max_length=200, null=True, blank=True, default='')
    network = models.CharField(max_length=200, null=True, blank=True, default='')
    DataSize = models.CharField(max_length=200, null=True, blank=True, default='')
    metertoken = models.CharField(max_length=1000, null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.orderid)


class Dstpackages(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200, default="")
    price = models.FloatField()

    def __str__(self):
        return str(self.name)


class GOtvpackages(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200, default="")
    price = models.FloatField()

    def __str__(self):
        return str(self.name)


class Startimespackages(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200, default="")
    price = models.FloatField()

    def __str__(self):
        return str(self.name)
