from .models import Shift
from django.db.models.signals import post_save,post_delete,pre_save
from django.dispatch import receiver
from . import views


from django.core.mail import send_mail


@receiver(pre_save, sender=Shift)
def shift_pre_save_receiver(sender, instance,**kwargs):
    if instance.id is None:
        print("This is from presave, I am creating shift now")
    else:
        previous = Shift.objects.get(id=instance.id)
        print("Hello from pre-save, Shift id ",previous.id, "has been updated")

@receiver(post_save, sender=Shift)
def shift_post_save_receiver(sender, instance,created,**kwargs):
    if created:
        id = instance.id
        print("This is from post save, shift id", id,"has been created")
        print("send email to blablabla")
    else:
        previous = Shift.objects.get(id=instance.id)
        print("This is from post save, Shift id ",previous.id, "has been updated")
 

@receiver(post_delete,sender=Shift)
def delete_shift(sender,instance,**kwargs):
    print("Shift has been deleted")




"""
def send_mail_to_user(sender, instance, created, **kwargs):
    if created:
        send_mail(
                'Subject here',
                'Here is the message.',
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
            )
"""