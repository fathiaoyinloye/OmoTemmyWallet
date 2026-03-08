from django.urls import path

import wallet
from .views import transfer_wallet

urlpatterns = [
    path('transfer/', transfer_wallet, name='transfer'),
]#'854a013c-c765-477b-9538-6541eba7500b'