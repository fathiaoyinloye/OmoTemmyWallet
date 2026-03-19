import wallet
from wallet.models import Wallet
from .models import Notification
from django.core.mail import send_mail

def create_notification(user):
    print(user.wallet.account_number)
    notification = Notification.objects.create(
        message=f"""
        Hi {user.first_name}, Welcome to OmoTemmyPay!
        Your wallet number is {user.wallet.wallet_number}
        your alternate wallet number is {user.wallet.account_number}     
        Thank you for using OmotemmyWallet!

""",
        wallet_number=user.wallet.account_number,
        event_type = "Wallet Created"
    )
    send_mail(

        subject="Welcome to OmoTemmyWallet!",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True,
    )
    notification.is_read =True
    notification.save()





def create_deposit_notification(user_wallet: Wallet, amount):
    notification = Notification.objects.create(
        message=f"Depoisit of {amount}  was successful",
        wallet_number=user_wallet.wallet_number,
        event_type="Deposit SUccess",
    )
    send_mail(#send mail is coming from django

        subject="Depoisit ALert",
        message=notification.message,
        from_email='',
        recipient_list=[user_wallet.user.email],
        fail_silently=True,
    )
    notification.is_read = True
    notification.save()