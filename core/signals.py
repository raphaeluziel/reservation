from .models import Shift
from django.db.models.signals import post_save,post_delete,pre_save
from django.dispatch import receiver



from django.core.mail import send_mail


@receiver(pre_save, sender=Shift)
def shift_pre_save_receiver(sender, instance,**kwargs):
    if instance.id is None:
        print(f"This is from presave, I am creating shift now,{sender},kwargs:{kwargs}")
        
    else:
        previous = Shift.objects.get(id=instance.id)
        print(f"Hello from pre-save, Shift id ,{previous.id}, has been updated,{sender},kwargs:{kwargs}")
        

@receiver(post_save, sender=Shift)
def shift_post_save_receiver(sender, instance,created,**kwargs):
    if created:
        id = instance.id
        print(f"This is from post save, shift {id} has been created,{sender},kwargs:{kwargs}")
        print(f"send email to blablabla,{sender},kwargs:{kwargs}")
        
 
    else:
        previous = Shift.objects.get(id=instance.id)
        print("This is from post save, Shift id ",previous.id, "has been updated")
        print(f"{sender},kwargs:{kwargs}")
 

@receiver(post_delete,sender=Shift)
def delete_shift(sender,instance,**kwargs):
    print(f"Shift has been deleted,{sender},kwargs:{kwargs}")




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