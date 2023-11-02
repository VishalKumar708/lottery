from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Lottery, User, LotteryUserMapping, LotteryPayment


class LotteryAdmin(admin.ModelAdmin):
    list_display = ['id', 'lotteryName', 'duration', 'amount', 'startDate', 'endDate', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate', 'updatedDate']
    list_filter = ('isActive',)

    @admin.action(description='Pivot Tabel')
    def custom_action_with_data(self, request, queryset):
        if len(queryset) != 1:
            return self.message_user(request, 'Please select only a single record.', level=messages.WARNING)

        obj = queryset[0]

        app2_view_url = reverse('kitty:pivotTable', kwargs={'lottery_id': obj.id})
        redirect_url = f"{app2_view_url}?original_url={request.path}"
        return redirect(redirect_url)

    actions = [custom_action_with_data]

admin.site.register(Lottery, LotteryAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phoneNumber', 'address', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate', 'updatedDate']


admin.site.register(User, UserAdmin)

from .forms import AddPaymentDetailsInBulk
class LotteryUserMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'lotteryId', 'userId', 'lotteryNumber', 'userName', 'additionalAmount', 'discount', 'gift', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate', 'updatedDate']
    list_filter = ('lotteryNumber', 'lotteryId', 'userId')

    @admin.action(description='Add Lottery Payment In Bulk')
    def custom_action_with_data(self, request, queryset):
        records = [obj.id for obj in queryset]
        request.session['queryset'] = records
        app2_view_url = reverse('kitty:addPaymentRecordInBulk')
        redirect_url = f"{app2_view_url}?original_url={request.path}"
        return redirect(redirect_url)

    @admin.action(description='show pending amount records')
    def show_pending_amount_records(self, request, queryset):
        # if len(queryset) == 0:
        #     return self.message_user(request, "Do not select any Record to perform this action.", level=messages.WARNING)
        app2_view_url = reverse('kitty:showDetailsOfPendingAmount')
        redirect_url = f"{app2_view_url}?original_url={request.path}"
        return redirect(redirect_url)

    actions = [custom_action_with_data, show_pending_amount_records]

    # list_display.insert(3, 'name')
    #
    # def name(self, obj):
    #     return obj.userId.name  # Assuming 'user_name' is a field in the User model
    # name.short_description = 'Member'


admin.site.register(LotteryUserMapping, LotteryUserMappingAdmin)


class LotteryPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'lotteryUserMappingId', 'amount', 'orderMonth', 'paymentMode', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate', 'updatedDate']
    list_filter = ('lotteryUserMappingId',)
admin.site.register(LotteryPayment, LotteryPaymentAdmin)
# Register your models here.
