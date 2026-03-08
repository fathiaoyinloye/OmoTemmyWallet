from django.db import transaction
from wallet.services.register_wallet import create_wallet
from user.services import create_user
from notification.services import create_notification

@transaction.atomic
def create_user_wallet(validated_data):
    user = create_user(validated_data)
    wallet = create_wallet(user)
    create_notification(user)
    return user,wallet