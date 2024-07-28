
from rest_framework.generics import ListAPIView,UpdateAPIView,CreateAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from ....models import ( Wallet, 
                       Telegram_User,
                       Deposit,
                       Withdraw,
                       )
from ..serializers import (WalletSerializer,
                          DepositSerializer,
                          withdrawSerializer,
                        )
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
import re
import jdatetime
from datetime import datetime


class WalletView(ListAPIView,UpdateAPIView,RetrieveAPIView):

    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        for wal in data:
            telegram_user_id = Telegram_User.objects.get(id = wal['telegram_user']).user_id
            wal['telegram_user'] = telegram_user_id
        return Response(data)


class DepositView(ListAPIView,UpdateAPIView):
    serializer_class = DepositSerializer
    queryset = Deposit.objects.all()
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        
        data = list(res.data)
        response = {}
        for pos in data:
            wallet = Wallet.objects.get(id = int(pos['wallet']))
            pos['wallet_name'] = wallet.name
            pos['balance'] = wallet.balance
            pattern = r"(.*?)T"
            text = pos['created_date']
            match = re.search(pattern, text)

            if match:
                pos['created_date'] = match.group(1)
                date_obj = datetime.strptime(match.group(1), "%Y-%m-%d")
                jalali_datetime = jdatetime.date.fromgregorian(date=date_obj)
                date_jalali = jalali_datetime.strftime("%Y-%m-%d")
                pos['created_date_shamsi'] = date_jalali
                pos['balance'] = wallet.balance
            if not pos['telegram_user'] in response.keys():
                response[pos['telegram_user']] = [pos]
            else:
                response[pos['telegram_user']].append(pos)

        return Response(response,status=status.HTTP_200_OK)

class Withdraw(ListAPIView,UpdateAPIView):
    serializer_class = withdrawSerializer
    queryset = Withdraw.objects.all()
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        
        data = list(res.data)
        response = {}
        for pos in data:
            wallet = Wallet.objects.get(id = int(pos['wallet']))
            pos['wallet_name'] = wallet.name
            pos['balance'] = wallet.balance
            pattern = r"(.*?)T"
            text = pos['created_date']
            match = re.search(pattern, text)

            if match:
                pos['created_date'] = match.group(1)
                date_obj = datetime.strptime(match.group(1), "%Y-%m-%d")
                jalali_datetime = jdatetime.date.fromgregorian(date=date_obj)
                date_jalali = jalali_datetime.strftime("%Y-%m-%d")
                pos['created_date_shamsi'] = date_jalali
                pos['balance'] = wallet.balance
            if not pos['telegram_user'] in response.keys():
                response[pos['telegram_user']] = [pos]
            else:
                response[pos['telegram_user']].append(pos)

        return Response(response,status=status.HTTP_200_OK)
