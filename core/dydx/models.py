from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import yfinance as yf
from datetime import datetime


class Telegram_User(models.Model):
    user_id = models.CharField(default="",max_length=500)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    uni_wallet = models.CharField(max_length=500)
    oneinch_wallet = models.CharField(default="",max_length=500)
    atomic_wallet = models.CharField(default="",max_length=500)
    created_date = models.DateTimeField(auto_now=True) 
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.username +" ( " + str(self.user_id) + " )"
    

class Positions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    telegram_user = models.CharField(default="",max_length=500)
    wallet = models.ForeignKey("Wallet",on_delete=models.CASCADE,null=True)
    make_position = models.ForeignKey("Makepositions",on_delete=models.CASCADE,null=True,blank=True)
    market = models.CharField(max_length=255,default='ETH-USD')
    long = models.BooleanField(default=True)
    size = models.FloatField()
    leverage = models.FloatField()
    realized_PL = models.FloatField()
    average_open = models.FloatField()
    channel_sent = models.BooleanField(default=False)
    channel_edited = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    

class Closed_Positions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    telegram_user = models.CharField(default="",max_length=500)
    wallet = models.ForeignKey("Wallet",on_delete=models.CASCADE,null=True)
    make_position = models.ForeignKey("Makepositions",on_delete=models.CASCADE,null=True,blank=True)
    market = models.CharField(max_length=255,default='ETH-USD')
    long = models.BooleanField(default=True)
    size = models.FloatField()
    leverage = models.FloatField()
    realized_PL = models.FloatField()
    average_open = models.FloatField()
    created_date = models.DateTimeField(auto_now=True)
    profit = models.FloatField()
    channel_sent = models.BooleanField(default=False)


class Wallet(models.Model):
    name = models.CharField(default="",max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    telegram_user = models.ForeignKey(Telegram_User,on_delete=models.CASCADE,null=True)
    balance= models.FloatField()
    account_leverage = models.FloatField(default=70)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    uniswap = models.BooleanField(default=True)
    wallet_address = models.CharField(max_length=500,null=True)
    uniswap_link = models.CharField(max_length=500,default="")
    oneinch_link = models.CharField(max_length=500,default="")

    def __str__(self) -> str:
        return self.name


class Makepositions(models.Model):
    market = models.CharField(max_length=255,default='ETH-USD')
    STATUS_CHOICES = (
        ('open', 'open'),
        ('close', 'close'),
    )
    position_status = models.CharField(default="open",max_length=256,choices=STATUS_CHOICES)
    long = models.BooleanField(default=True)
    ratio = models.FloatField()
    leverage = models.FloatField()
    realized_PL = models.FloatField()
    average_open = models.FloatField()
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id + 1000)


class Staking(models.Model):
    wallet = models.ForeignKey(Wallet,default=1,on_delete=models.CASCADE)
    telegram_user = models.CharField(default="",max_length=500)
    staking_volume = models.FloatField()
    staking_date = models.IntegerField()
    created_date = models.DateField()

    def __str__(self) -> str:
        return self.wallet.name + ' ( ' + str(self.staking_volume) + ' - ' + str(self.staking_date) + ' )'


class HistoryTrades(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    make_position = models.ForeignKey(Makepositions,on_delete=models.CASCADE,null=True,blank=True)
    time= models.CharField(max_length=256)
    market = models.CharField(max_length=256,default='ETH-USD')
    long = models.BooleanField(default=True)
    amount = models.CharField(max_length=256)
    price = models.CharField(max_length=256)
    total = models.CharField(max_length=256)
    fee = models.CharField(max_length=256)
    TRADETYPE_CHOICES = (
        ('Liquidated', 'Liquidated'),
        ('Market', 'Market'),
    )
    LIQUIDITY_CHOICES = (
        ('Maker', 'Maker'),
        ('Taker', 'Taker'),
    )
    tradetype = models.CharField(max_length=256,choices=TRADETYPE_CHOICES)
    liquidity = models.CharField(max_length=256,choices=LIQUIDITY_CHOICES)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    creation_time = models.DateField(null=True)
    def __str__(self) -> str:
        return str(self.make_position.id +1000)

class HistoryTransfers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time= models.CharField(max_length=256)
    action = models.CharField(max_length=256,default='Slow Withdraw')
    status = models.CharField(max_length=256, default='Confirmed')
    amount = models.CharField(max_length=256)
    transaction = models.CharField(max_length=500)
    transaction_link = models.CharField(max_length=500,default="https://")
    fee = models.CharField(max_length=256,default='-')
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    creation_time = models.DateField(null=True)


class HistoryFunding(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time= models.CharField(max_length=256)
    market = models.CharField(max_length=256,default='ETH-USD')
    funding_rate = models.CharField(max_length=500)
    long = models.BooleanField(default=True)
    payment = models.CharField(max_length=500)
    ppsition = models.CharField(max_length=500)
    position_asset = models.CharField(max_length=256,default='ETH')
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    creation_time = models.DateField(null=True)

class Deposit(models.Model):
    telegram_user = models.ForeignKey(Telegram_User,on_delete=models.CASCADE,null=True)
    volume = models.FloatField()
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    WALLET_CHOICES = (
        ('1Inch', '1Inch'),
        ('Uniswap', 'Uniswap'),
    )
    wallettype = models.CharField(default="Uniswap",max_length=256,choices=WALLET_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    channel_sent = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.wallet.name

class Withdraw(models.Model):
    telegram_user = models.ForeignKey(Telegram_User,on_delete=models.CASCADE,null=True)
    volume = models.FloatField()
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    WALLET_CHOICES = (
        ('1Inch', '1Inch'),
        ('Uniswap', 'Uniswap'),
    )
    wallettype = models.CharField(default="Uniswap",max_length=256,choices=WALLET_CHOICES)
    channel_sent = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.wallet.name
    
class Telegram_channel(models.Model):
    name = models.CharField(default="",max_length=255)
    user_telegram = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class HistoryFunding(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time= models.CharField(max_length=256)
    market = models.CharField(max_length=256,default='ETH-USD')
    funding_rate = models.CharField(max_length=500)
    long = models.BooleanField(default=True)
    payment = models.CharField(max_length=500)
    ppsition = models.CharField(max_length=500)
    position_asset = models.CharField(max_length=256,default='ETH')
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    creation_time = models.DateField(null=True)



@receiver(post_save, sender=Makepositions)
def make_positions(sender, instance, created, **kwargs):
    """
    Signal for post creating a user which
    activates when a user being created ONLY
    """
    all_wallets = Wallet.objects.all()
    if created:
        if instance.position_status == "open":
            for wallet in all_wallets:
                size = round(instance.ratio*wallet.balance*instance.leverage/instance.average_open,2)
                if size == 0:
                    continue
                Positions.objects.create(user = wallet.user,
                                        make_position=instance,
                                        telegram_user = wallet.telegram_user.user_id,
                                        wallet=wallet,
                                        market = instance.market,
                                        long = instance.long,
                                        size =size,
                                        leverage = instance.leverage,
                                        realized_PL = instance.realized_PL,
                                        average_open = instance.average_open,)
                HistoryTrades.objects.create(
                    user = wallet.user,
                    time= "",
                    make_position=instance,
                    market = instance.market,
                    long = instance.long,
                    amount = size,
                    price = instance.average_open,
                    total = round((instance.ratio*wallet.balance*instance.leverage),2),
                    fee = instance.realized_PL,
                    tradetype = "Market",
                    liquidity = "Taker",
                    creation_time = datetime.now().date()
                )
    
    else:
        if instance.position_status == "open":
            for wallet in all_wallets:
                size = round(instance.ratio*wallet.balance*instance.leverage/instance.average_open,2)
                if size == 0:
                    continue
                pos = Positions.objects.filter(user = wallet.user,make_position=instance)
                if len(pos)>0:
                    pos = pos[0]
                    pos.market = instance.market
                    pos.long = instance.long
                    pos.size =size
                    pos.leverage =instance.leverage
                    pos.realized_PL = instance.realized_PL
                    pos.average_open = instance.average_open
                    pos.channel_edited = False
                    pos.save()

        if instance.position_status == "close":
            eth = yf.Ticker('ETH-USD')
            allprice = eth.history()
            price = allprice['Close'].iloc[-1]
           
            for wallet in all_wallets:
                size = round(instance.ratio*wallet.balance*instance.leverage/instance.average_open,2)
                if size == 0:
                    continue
                if instance.long :
                    up = (price - instance.average_open)* size
                else:
                    up = (instance.average_open - price)*size
                profit = round(up,2)
                pos = Positions.objects.filter(user = wallet.user,make_position=instance)
                if len(pos)==0:
                    continue
                pos = pos[0]

                Closed_Positions.objects.create(user = wallet.user,
                                        make_position=instance,
                                        telegram_user = wallet.telegram_user.user_id,
                                        wallet=wallet,
                                        market = instance.market,
                                        long = instance.long,
                                        size =size,
                                        leverage = instance.leverage,
                                        realized_PL = instance.realized_PL,
                                        average_open = instance.average_open,
                                        profit = profit)

                HistoryTrades.objects.create(
                    user = wallet.user,
                    make_position=instance,
                    time= "",
                    market = instance.market,
                    long = not instance.long,
                    amount = size,
                    price = round(price,2),
                    total = round(size*price,2),
                    fee = instance.realized_PL,
                    tradetype = "Market",
                    liquidity = "Taker",
                    creation_time = datetime.now().date()
                )
                wallet.balance = wallet.balance + profit
                wallet.save()
                pos.delete()