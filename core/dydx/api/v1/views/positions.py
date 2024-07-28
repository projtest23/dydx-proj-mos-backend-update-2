
from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from ....models import (Positions, 
                       Wallet, 
                       Makepositions,
                       Closed_Positions,
                       HistoryTrades
                       )
from ..serializers import (PositionSerializer,
                          AllpositionsSerializer,
                          OpenPositionChannelSerializer,
                          closedPositionChannelSerializer
                        )
import yfinance as yf
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response

import re
import jdatetime
from datetime import datetime


class PositionsView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PositionSerializer
    # queryset = Positions.objects.all()

    def get_queryset(self):

        queryset = Positions.objects.filter(user=self.request.user).order_by('-created_date')

        return queryset

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        data = list(res.data)
        user = self.request.user
        eth = yf.Ticker('ETH-USD')
        allprice = eth.history()
        price = allprice['Close'].iloc[-1]
        balancedata = Wallet.objects.filter(user=user)
        if len(balancedata)<1:
            return res
        

        balancedata=balancedata[0]
        balance = balancedata.balance
        uniswap = balancedata.uniswap
        wallet = balancedata.wallet_address
        account_leverage = balancedata.account_leverage
        up_total = 0
        size_d_total = 0

        if len(data)<1:
            data_dict = {}
            data_dict['margin_usage'] = 0
            data_dict['balance'] = balance
            data_dict['uniswap'] = uniswap
            data_dict['wallet'] = wallet
            data_dict['account_leverage'] = account_leverage
            data_dict['equity'] = balance
            data_dict['bying_power'] = round((balance*20),2)
            data.append(data_dict)
            return Response(data)


        for pos in data:
            
            average_open = pos['average_open']
            size = pos['size']
            long = pos['long']
            if long :
                up = (price - average_open)* size
            else:
                up = (average_open - price)*size
            up_total += up
            size_d_total += size*price
            pos['unrealized_profit'] = round(up,2)
            size_dollar = size*price
            pos['size_dollar'] = round(size_dollar,2)
            pos['un_profit_perc'] = round((up*100/size_dollar),2)

        for pos in data:
            average_open = pos['average_open']
            size = pos['size']
            long = pos['long']
            if long :
                liq_price = average_open-(balance/size)
                up = (price - average_open)* size
            else:
                liq_price = average_open + (balance/size)
                up = (average_open - price)*size
            if liq_price <0 :
                liq_price = 0
            pos['liq_price'] = round(liq_price,2)
            pos['oracle'] = round(price,2)
            pos['bying_power'] = round((balance*20),2)
            pos['equity'] = round((balance + up_total),2) 
            pos['margin_usage'] = round(((size_d_total/account_leverage)*100/balance),2)
            pos['balance'] = balance
            pos['account_leverage'] = account_leverage
            pos['uniswap'] = uniswap
            pos['wallet'] = wallet
        return Response(data)


class AllPositionsView(CreateAPIView,ListAPIView):

    serializer_class = AllpositionsSerializer
    queryset = Positions.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.validated_data
        telegram_user = serializer['telegram_user']
        wallet = serializer['wallet']
        data = Positions.objects.filter(telegram_user = telegram_user)
        eth = yf.Ticker('ETH-USD')
        allprice = eth.history()
        price = allprice['Close'].iloc[-1]
        balancedata = Wallet.objects.get(id=int(wallet.id))
        
        if not balancedata:
            return Response('You have no active wallet',status=status.HTTP_400_BAD_REQUEST)

        balance = balancedata.balance


        if len(data)<1:
            return Response("You have no open position",status=status.HTTP_400_BAD_REQUEST)

        for pos in data:
            average_open = pos.average_open
            size = pos.size
            long = pos.long
            up = 0
            make_pos = Makepositions.objects.get(id=pos.make_position.id)
            if long :
                up = (price - average_open)* size
            else:
                up = (average_open - price)*size

            balancedata.balance = balance + up
            balancedata.save()
            Closed_Positions.objects.create(
                user = wallet.user,
                        make_position=pos.make_position,
                        telegram_user = pos.telegram_user,
                        wallet=wallet,
                        market = pos.market,
                        long = long,
                        size =size,
                        leverage = pos.leverage,
                        realized_PL = pos.realized_PL,
                        average_open = average_open,
                        profit = up
            )
            HistoryTrades.objects.create(
                    user = wallet.user,
                    time= "",
                    market = pos.market,
                    long = long,
                    amount = size,
                    price = average_open,
                    total = make_pos.ratio*balance*average_open,
                    fee = pos.realized_PL,
                    tradetype = "Market",
                    liquidity = "Taker",
                    creation_time = datetime.now().date()
                )
            pos.delete()

        return Response("All positions has been closed",status=status.HTTP_200_OK)

class closedPositionChannel(ListAPIView,UpdateAPIView):
    serializer_class = closedPositionChannelSerializer
    # queryset = Positions.objects.all()

    def get_queryset(self):

        queryset = Closed_Positions.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        data = list(res.data)
        response = {}
        
        for pos in data:
            wallet = Wallet.objects.get(id = int(pos['wallet']))
            make_position = Makepositions.objects.get(id = int(pos['make_position']))
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
                pos['size_channel'] = make_position.ratio * wallet.balance
            if not pos['telegram_user'] in response.keys():
                response[pos['telegram_user']] = [pos]
            else:
                response[pos['telegram_user']].append(pos)

        return Response(response,status=status.HTTP_200_OK)


class OpenPositionChannel(ListAPIView,UpdateAPIView):
    serializer_class = OpenPositionChannelSerializer
    # queryset = Positions.objects.all()

    def get_queryset(self):

        queryset = Positions.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        data = list(res.data)
        response = {}
        
        for pos in data:
            wallet = Wallet.objects.get(id = int(pos['wallet']))
            make_position = Makepositions.objects.get(id = int(pos['make_position']))
            pos['wallet_name'] = wallet.name
            pattern = r"(.*?)T"
            text = pos['created_date']
            match = re.search(pattern, text)

            if match:
                pos['created_date'] = match.group(1)
                date_obj = datetime.strptime(match.group(1), "%Y-%m-%d")
                jalali_datetime = jdatetime.date.fromgregorian(date=date_obj)
                date_jalali = jalali_datetime.strftime("%Y-%m-%d")
                pos['created_date_shamsi'] = date_jalali
                pos['size_channel'] = make_position.ratio * wallet.balance
            if not pos['telegram_user'] in response.keys():
                response[pos['telegram_user']] = [pos]
            else:
                response[pos['telegram_user']].append(pos)

        return Response(response,status=status.HTTP_200_OK)