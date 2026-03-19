from django.urls import path

import wallet
from .views import transfer_wallet, dashboard, deposit_wallet

urlpatterns = [
    path('transfer/', transfer_wallet, name='transfer'),
    path('dashboard/', dashboard,name='dashboard'),
    path('deposit/', deposit_wallet, name='deposit'),

]