from django.contrib.auth import get_user_model

user = get_user_model()

def initiate_paystack_payment(pay_user, amount):
    header = {
        "Authorization": f"Bearer {pay_user.token}",
    }