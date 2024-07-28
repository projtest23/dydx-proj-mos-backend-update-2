from django.urls import path
from . import views

app_name = "api-v1"

urlpatterns = [
    path('positions/',views.PositionsView.as_view(),name="post-list"),
    path('openpositions/',views.OpenPositionChannel.as_view(),name="openpositions"),
    path('openpositions/<int:pk>/',views.OpenPositionChannel.as_view(),name="openpositions"),
    path('closedposition/',views.closedPositionChannel.as_view(),name="closedposition"),
    path('closedposition/<int:pk>/',views.closedPositionChannel.as_view(),name="closedposition-update"),
    path('wallet/<int:pk>/',views.WalletView.as_view(),name="wallet_edit"),
    path('wallet/',views.WalletView.as_view(),name="wallet"),
    path('staking/',views.StakingView.as_view(),name="staking"),
    path('telegramuser/',views.telegramuserView.as_view(),name="telegramuser"),
    path('allpositions/',views.AllPositionsView.as_view(),name="allpositions"),
    path('historytransfers/',views.HistoryTransferView.as_view(),name="history-transfers"),
    path('historytrades/',views.HistoryTradesView.as_view(),name="history-trades"),
    path('historyfundings/',views.HistoryFundingView.as_view(),name="history-fundings"),
    path('telegramchannel/',views.TelegramChannelView.as_view(),name="telegramchannel"),
    path('deposit/',views.DepositView.as_view(),name="deposit"),
    path('deposit/<int:pk>/',views.DepositView.as_view(),name="deposit-update"),
    path('withdraw/',views.Withdraw.as_view(),name="withdraw"),
    path('withdraw/<int:pk>/',views.Withdraw.as_view(),name="withdraw-update"),
]