from time import sleep

# # Common approach - High Coupling
# from config.celery import celery


# @celery.task
# def notify_customers(message):
#     print(f'\nSending 10k emails...\n')
#     print(f'\n{message = }\n')
#     sleep(4)
#     print('Emails were successfully sent!')
    
# Better approach with low coupling -------------

from celery import shared_task 


@shared_task
def notify_customers(message):
    print(f'\nSending 10k emails...\n')
    print(f'\n{message = }\n')
    sleep(4)
    print('Emails were successfully sent!')