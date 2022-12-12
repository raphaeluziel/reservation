import logging

from django.core.mail import EmailMessage
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .models import Shift,CustomUser,Nurse, Employer, AddressBook
from core.logging.logging_config import logger
from decouple import config
import datetime
from django.utils import timezone
from datetime import datetime, date, time


EMAIL_ADDRESS_1 = config("EMAIL_ADDRESS_1")
EMAIL_ADDRESS_2 = config("EMAIL_ADDRESS_2")


@receiver(pre_save, sender=Shift)
def shift_pre_save_receiver(sender, instance, **kwargs):

    logger.info("shift_pre_save_receiver() function called")

    # Save the original values of the fields
    instance._original_nurse = instance.nurse
    instance._original_employer = instance.employer
    instance._original_address = instance.address
    instance._original_status = "Open"
    instance._original_role = instance.role
    instance._original_user = instance.user
    instance._original_start_time = instance.start_time
    instance._original_finish_time = instance.finish_time
    instance._original_details = instance.details



    # Check if any of the fields have changed
    for field in ["nurse", "employer", "address", "status", "role", "user", "start_time", "finish_time", "details"]:
        if getattr(instance, field) != getattr(instance, f"_original_{field}"):
            # Log the changed field
            logger.info(f"Shift with id {instance.id} has changed field {field} to {getattr(instance, field)} (changed by {instance.user} at {datetime.now()})")

@receiver(post_save, sender=Shift)
def shift_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        # Shift was created
        subject = "Shift created"
        message = f"Shift with id {instance.id} was created by {instance.user}."

    elif instance.status=="Reserved" and instance.status != instance._original_status:
        # Shift was reserved
        subject = "Shift reserved"
        message = f"Shift with id {instance.id} was reserved by {instance.user}."
      
    else:
        # Shift was updated
        subject = "Shift updated"
        message = f"Shift with id {instance.id} was updated by {instance.user}."

    recipients = [EMAIL_ADDRESS_1, EMAIL_ADDRESS_2] 
    email = EmailMessage(subject, message, to=recipients)
    email.send()


@receiver(post_delete, sender=Shift)
def delete_shift(sender, instance, **kwargs):
   
    logger.info(f"Shift with id {instance.id} was deleted by {instance.user}")
    subject = "Shift deleted"
    message = f"Shift with id {instance.id} was deleted by {instance.user}"
    recipients = [EMAIL_ADDRESS_1, EMAIL_ADDRESS_2]
    
    email = EmailMessage(subject, message, to=recipients)
    email.send()


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




