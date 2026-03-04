import wallet
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