import random


def generate_account_number():
    return "44" + str(random.randrange(000000000, stop=999999))



def generate_reference():
    return "REF" + str(random.randrange(000000000, stop=999999))