
from django.core.mail import send_mail
from celery import shared_task

from me import settings


@shared_task()
def email_task(subject, message):
    """Sends an email when the feedback form has been submitted."""
     # Simulate expensive operation(s) that freeze Django
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['parasmodi100@gmail.com']
    send_mail(subject, message, email_from, recipient_list, fail_silently=False,)


    return None