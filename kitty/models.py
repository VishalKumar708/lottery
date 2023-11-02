
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    isActive = models.BooleanField(default=True)
    groupId = models.CharField(max_length=40, default=1)
    createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='%(class)s_created')
    updatedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated')
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user passed as an argument (if any)
        if user:
            if not self.createdBy:
                self.createdBy = user
            self.updatedBy = user
        super(BaseModel, self).save(*args, **kwargs)


class Lottery(BaseModel):
    id = models.BigAutoField(primary_key=True)
    lotteryName = models.CharField(max_length=30)
    duration = models.IntegerField()
    amount = models.FloatField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if not self.endDate:
            self.endDate = self.startDate + timedelta(days=((self.duration)-1)*30)
        super(Lottery, self).save(*args, **kwargs)

    def __str__(self):
        return self.lotteryName


class User(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=10)
    address = models.CharField(max_length=70)

    # def save(self, *args, **kwargs):
    #     pass

    def __str__(self):
        return str(self.id)


class LotteryUserMapping(BaseModel):
    id = models.BigAutoField(primary_key=True)
    lotteryId = models.ForeignKey(Lottery, on_delete=models.SET_NULL, null=True)
    userId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lotteryNumber = models.IntegerField()
    userName = models.CharField(max_length=50, blank=True)
    additionalAmount = models.FloatField(null=True, blank=True)
    discount = models.FloatField(default=0)
    gift = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.userName:
            try:
                user_obj = User.objects.get(id=self.userId.id)  # Get the ID of the associated User
                self.userName = user_obj.name
            except User.DoesNotExist:
                raise ValueError({'userId': ['Please enter a valid userId.']})

        super(LotteryUserMapping, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class LotteryPayment(BaseModel):
    PAYMENT_MODE = (
        ('C', 'Cash'),
        ('O', 'Online'),
    )
    id = models.BigAutoField(primary_key=True)
    lotteryUserMappingId = models.ForeignKey(LotteryUserMapping, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    orderMonth = models.DateField()
    paymentMode = models.CharField(max_length=1, choices=PAYMENT_MODE)




# Create your models here.
