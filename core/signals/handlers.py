
from django.dispatch import receiver 

from store.signals import order_created
# from store.serializers import CreateOrderSerializer



@receiver(order_created)
def on_order_created(sender, **kwargs):
    print(f'\n\nSIGNAL order_created received\n{kwargs['order'] = }\n\n') 