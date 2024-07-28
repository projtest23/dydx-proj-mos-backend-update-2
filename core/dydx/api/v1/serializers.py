from rest_framework.serializers import ModelSerializer
from ...models import (
        Positions,
        HistoryTransfers,
        HistoryTrades,
        HistoryFunding,
        Staking,
        Telegram_User,
        Wallet,
        Telegram_channel,
        Deposit,
        Closed_Positions
)

class PositionSerializer(ModelSerializer):

    class Meta:
        model = Positions
        fields = [
            "id",
            "user",
            "market",
            "long",
            "size",
            "leverage",
            "realized_PL",
            "average_open",
            "created_date",
            "updated_date",
        ]


    def to_representation(self, instance):
        rep = super().to_representation(instance)
    
        return rep
    
class HistoryTradesSerializer(ModelSerializer):

    class Meta:
        model = HistoryTrades
        fields = [
            "id",
            "user",
            "time",
            "market",
            "long",
            "amount",
            "price",
            "total",
            "fee",
            "tradetype",
            "liquidity",
            "created_date",
            "updated_date",
            'creation_time'
        ]
    
class HistoryTransferSerializer(ModelSerializer):

    class Meta:
        model = HistoryTransfers
        fields = [
            "id",
            "user",
            "time",
            "action",
            "status",
            "amount",
            "transaction",
            "transaction_link",
            "fee",
            "created_date",
            "updated_date",
            'creation_time'
        ]


    def to_representation(self, instance):
        rep = super().to_representation(instance)
    
        return rep
    
class HistoryFundingSerializer(ModelSerializer):

    class Meta:
        model = HistoryFunding
        fields = [
            "id",
            "user",
            "time",
            "market",
            "funding_rate",
            "long",
            "payment",
            "ppsition",
            "position_asset",
            "created_date",
            "updated_date",
            'creation_time'
        ]


    def to_representation(self, instance):
        rep = super().to_representation(instance)
    
        return rep

  
class StakingSerializer(ModelSerializer):

    class Meta:
        model = Staking
        fields = [
            "id",
            "wallet",
            "telegram_user",
            "staking_volume",
            "staking_date",
            "created_date"
        ]

class TelegramUserSerializer(ModelSerializer):

    class Meta:
        model = Telegram_User
        fields = [
            "id",
            "user_id",
            "username",
            "password",
            "atomic_wallet",
            "oneinch_wallet",
            "uni_wallet"
        ]

class AllpositionsSerializer(ModelSerializer):

    class Meta:
        model = Positions
        fields = [
            "telegram_user",
            "wallet"
        ]

class WalletSerializer(ModelSerializer):

    class Meta:
        model = Wallet
        fields = [
            "id",
            "name",
            "user",
            "telegram_user",
            "balance",
            "account_leverage",
            "uniswap",
            "wallet_address",
            "oneinch_link",
            "uniswap_link"
        ]

class DepositSerializer(ModelSerializer):

    class Meta:
        model = Deposit
        fields = [
            "id",
            "telegram_user",
            "wallet",
            "volume",
            "wallettype",
            "channel_sent",
            "oneinch_link",
            "uniswap_link",
            "created_date"
            
        ]

class withdrawSerializer(ModelSerializer):

    class Meta:
        model = Deposit
        fields = [
            "id",
            "telegram_user",
            "wallet",
            "volume",
            "wallettype",
            "channel_sent",
            "created_date"
            
        ]

class TelegramChannelSerializer(ModelSerializer):

    class Meta:
        model = Telegram_channel
        fields = [
            "user_telegram",
            "channel_id"
        ]

class OpenPositionChannelSerializer(ModelSerializer):

    class Meta:
        model = Positions
        fields = [
            "id",
            "telegram_user",
            "make_position",
            "wallet",
            "long",
            "size",
            "channel_sent",
            "channel_edited",
            "average_open",
            "created_date",
        ]

class closedPositionChannelSerializer(ModelSerializer):

    class Meta:
        model = Closed_Positions
        fields = [
            "id",
            "telegram_user",
            "make_position",
            "wallet",
            "long",
            "size",
            "average_open",
            "created_date",
            "profit",
            "channel_sent"
        ]