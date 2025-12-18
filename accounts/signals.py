from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save,sender=User)
def send_welcome_email(sender,instance,created,**kwargs):
    if created and hasattr(instance,'role') and instance.role == 'student':
        subject = "WelcomeTo Student Job portal"
        message = f"Hi{instance.full_name},\n\n Thank You signing up as a student on Job Portal \n"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        send_mail(subject,message,from_email,recipient_list)
        print(f"Welcome Email Sent to {instance.email}")