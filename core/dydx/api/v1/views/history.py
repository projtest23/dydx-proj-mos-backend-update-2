
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ....models import ( HistoryTransfers, 
                       HistoryFunding, 
                       HistoryTrades, 

                       )
from ..serializers import (HistoryTradesSerializer,
                          HistoryFundingSerializer,
                          HistoryTransferSerializer,
                        )
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.settings import api_settings
from datetime import datetime


class HistoryTradesView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = HistoryTradesSerializer
    # queryset = Positions.objects.all()

    def get_queryset(self):

        queryset = HistoryTrades.objects.filter(user=self.request.user).order_by('-created_date')

        return queryset
    
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        data = list(res.data)
        now = datetime.now().date()
        for trade in data:
            creation_time = datetime.strptime(trade['creation_time'], "%Y-%m-%d").date()
            diff = (now-creation_time).days
            if diff<1:
                trade['time'] = f'1d'
            elif diff<7:
                trade['time'] = f'{diff}d'
            elif diff<700:
                trade['time'] = f'{int(diff/7)}w'
            else:
                trade['time'] = f'{int(diff/30)}M'
        # print(data)
        return Response(data)

class HistoryTransferView(ListAPIView):


    permission_classes = [IsAuthenticated]
    serializer_class = HistoryTransferSerializer
    # queryset = Positions.objects.all()

    def get_queryset(self):

        queryset = HistoryTransfers.objects.filter(user=self.request.user).order_by('-created_date')

        return queryset
    
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        data = list(res.data)
        now = datetime.now().date()
        for trade in data:
            creation_time = datetime.strptime(trade['creation_time'], "%Y-%m-%d").date()
            diff = (now-creation_time).days
            if diff<1:
                trade['time'] = f'1d'
            elif diff<7:
                trade['time'] = f'{diff}d'
            elif diff<700:
                trade['time'] = f'{int(diff/7)}w'
            else:
                trade['time'] = f'{int(diff/30)}M'
        # print(data)
        return Response(data)


class HistoryFundingView(ListAPIView):


    permission_classes = [IsAuthenticated]
    serializer_class = HistoryFundingSerializer
    # queryset = Positions.objects.all()

    def get_queryset(self):

        queryset = HistoryFunding.objects.filter(user=self.request.user).order_by('-created_date')

        return queryset
    
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        data = list(res.data)
        now = datetime.now().date()
        for trade in data:
            creation_time = datetime.strptime(trade['creation_time'], "%Y-%m-%d").date()
            diff = (now-creation_time).days
            if diff<1:
                trade['time'] = f'1d'
            elif diff<7:
                trade['time'] = f'{diff}d'
            elif diff<700:
                trade['time'] = f'{int(diff/7)}w'
            else:
                trade['time'] = f'{int(diff/30)}M'
        # print(data)
        return Response(data)

