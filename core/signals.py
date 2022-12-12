import logging

from django.core.mail import send_mail, EmailMessage
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .models import Shift,CustomUser


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Shift)
def shift_post_save_receiver(sender, instance, created, **kwargs):
   
    if created:
        # Shift was created
        subject = "Shift created"
        message = f"Shift with id {instance.id} by {instance.user}"
        recipients = ["yi.yuan.glo@gmail.com", "yi.yuan.new@gmail.com"]
        email = EmailMessage(subject, message, to=recipients)
        email.send()
    else:
        """
        # Shift was updated
        # Get the list of fields that have been updated
        updated_fields = []
        previous = Shift.objects.get(id=instance.id)
        for field in instance._meta.fields:
            # Check if the field has been updated
            if instance.has_changed(field.name):
          
                # The field has been updated
                updated_fields.append(field.name)
        """
        subject = "Shift updated"
        message = f"Shift with id {instance.id} was updated by {instance.user}."
        recipients = ["yi.yuan.glo@gmail.com", "yi.yuan.new@gmail.com"]
        email = EmailMessage(subject, message, to=recipients)
        email.send()



@receiver(post_delete, sender=Shift)
def delete_shift(sender, instance, **kwargs):
       
    logger.info(f"Shift with id {instance.id} was deleted by {instance.user}")
    subject = "Shift deleted"
    message = f"Shift with id {instance.id} was deleted by {instance.user}"
    recipients = ["yi.yuan.glo@gmail.com", "yi.yuan.new@gmail.com"]
    email = EmailMessage(subject, message, to=recipients)
    email.send()







