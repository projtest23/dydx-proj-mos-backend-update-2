
from rest_framework.generics import ListAPIView,UpdateAPIView,CreateAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from ....models import ( Wallet, 
                       Staking,
                       Telegram_User,
                       Telegram_channel
                       )
from ..serializers import (StakingSerializer,
                          TelegramUserSerializer,
                          TelegramChannelSerializer
                        )
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from datetime import datetime


class StakingView(ListAPIView,CreateAPIView,UpdateAPIView):

    serializer_class = StakingSerializer
    queryset = Staking.objects.all()
    
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        data = list(res.data)
        now = datetime.now().date()
        for stake in data:
            creation_time = datetime.strptime(stake['created_date'], "%Y-%m-%d").date()
            days_left = stake["staking_date"]*30 - (now - creation_time).days
        # print(data)
            if days_left<0:
                stake['days_left'] = 0
            else:
                stake['days_left'] = days_left
        return Response(data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data['telegram_user']
        user_wallet = Wallet.objects.get(id = data['wallet'].id)
        old_staking = Staking.objects.filter(telegram_user=user,wallet=data['wallet'])
        balance = user_wallet.balance
        if old_staking:
            for stake in old_staking:
                balance = balance - stake.staking_volume

        if data['staking_volume']>balance:
            return Response(f"your balance is short", status=status.HTTP_400_BAD_REQUEST)


        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class telegramuserView(ListAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView):

    serializer_class = TelegramUserSerializer
    queryset = Telegram_User.objects.all()


class TelegramChannelView(ListAPIView):
    serializer_class = TelegramChannelSerializer
    queryset = Telegram_channel.objects.all()
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        data = list(res.data)
        response = {}
        for tel in data:
            if not tel['user_telegram'] in response.keys():
                response[tel['user_telegram']] = tel
        return Response(response,status=status.HTTP_200_OK)


