from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job, UserRecords

@receiver(post_save, sender=Job)
def update_customer_type_after_job(sender, instance, created, **kwargs):
    '''
    this handle the situation where new job are created amd we need 
    to update the customer type of the user.
    '''
    if created:
        user = instance.user
        user.customer_type = user._calculate_customer_type()  
        user.save()  
