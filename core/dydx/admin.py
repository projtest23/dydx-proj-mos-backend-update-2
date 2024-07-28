from django.contrib import admin
from .models import (Positions,
                     Wallet,
                     HistoryFunding, 
                     HistoryTrades, 
                     HistoryTransfers,
                     Makepositions, 
                     Telegram_User,
                     Staking,
                     Telegram_channel,
                     Deposit,
                     Withdraw,
                     Closed_Positions)



class PositionsAdmin(admin.ModelAdmin):
    list_display = ('user','market', 'long', 'average_open','created_date')
    list_filter = ('user','long','created_date')
    search_fields = ['user', 'long']


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user','balance','created_date')
    list_filter = ('user','balance')
    search_fields = ['user', 'balance']

admin.site.register(Positions,PositionsAdmin)
admin.site.register(Wallet,BalanceAdmin)
admin.site.register(HistoryFunding)
admin.site.register(HistoryTrades)
admin.site.register(HistoryTransfers)
admin.site.register(Makepositions)
admin.site.register(Telegram_User)
admin.site.register(Staking)
admin.site.register(Telegram_channel)
admin.site.register(Deposit)
admin.site.register(Withdraw)
admin.site.register(Closed_Positions)