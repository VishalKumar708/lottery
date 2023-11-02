from django import forms

from .models import Lottery


def lottery_drop_down():
    qs = Lottery.objects.all().values('id', 'lotteryName')

    return [(lottery['id'], lottery['lotteryName']) for lottery in qs]


class AddPaymentDetailsInBulk(forms.Form):
    PAYMENT_MODE = (
        ('C', 'Cash'),
        ('O', 'Online'),
    )
    # # lotteryId = forms.ChoiceField(choices=lottery_drop_down(), label="select lottery")
    # amount = forms.FloatField()
    # orderMonth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # paymentMode = forms.ChoiceField(choices=PAYMENT_MODE, label="Select Payment Mode")

    amount = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'})
    )
    orderMonth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select Date'}),
        label='Order Month'  # Add a label for the 'orderMonth' field
    )
    paymentMode = forms.ChoiceField(
        choices=PAYMENT_MODE,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Payment Mode"
    )

