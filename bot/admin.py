from django.contrib import admin
from .models import Users, PaySystems, Enter, Withdrawal
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver





class UsersAdmin(admin.ModelAdmin):
	fields = ['username', 'id_user', 'balance', 'date_reg']
	list_display = ('username', 'id_user', 'balance', 'date_reg')

admin.site.register(Users, UsersAdmin)

class PaySystemsAdmin(admin.ModelAdmin):
	fields = ['ps_name','ps_abbr','ps_purse']
	list_display = ('ps_name','ps_abbr','ps_purse')

admin.site.register(PaySystems, PaySystemsAdmin)

class EnterAdmin(admin.ModelAdmin):
	fields = ['username', 'en_id','en_ps','en_date','en_sum','en_status']
	list_display = ('username', 'en_id','en_ps','en_date','en_sum','en_status')
admin.site.register(Enter, EnterAdmin)

class WithdrawalAdmin(admin.ModelAdmin):
	fields = ['username', 'wd_id','wd_ps','wd_date','wd_sum','wd_status']
	list_display = ('username', 'wd_id','wd_ps','wd_date','wd_sum','wd_status')
admin.site.register(Withdrawal, WithdrawalAdmin)

@receiver(post_save, sender = Enter)
def enter_balance(sender, instance, **kwargs):
	status = instance.en_status
	balance = instance.balance
	if status == 2 and instance.en_sum:
		user = instance.username
		user = balance + instance.en_sum
		user.save()