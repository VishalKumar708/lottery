from django.urls import path
from .views import process_payment, PivotTable, showDetailsOfPendingAmount
app_name = 'kitty'
urlpatterns = [
    path('addPaymentRecordInBulk/', process_payment, name='addPaymentRecordInBulk'),
    path('pivotTable/<slug:lottery_id>/', PivotTable.as_view(), name='pivotTable'),
    path('showDetailsOfPendingAmount/', showDetailsOfPendingAmount.as_view(), name='showDetailsOfPendingAmount')
]
