from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from website.models import Job, UserRecords
from django.db import transaction

@receiver(post_save, sender=Job)
def update_customer_type_after_job(sender, instance, created, **kwargs):
    '''
    This handles the situation where a new job is created or an existing job is updated,
    and we need to update the customer type of the user.
    '''
    user = instance.user
    user.customer_type = user._calculate_customer_type()
    print(f"-----User {user.name} updated to {user.customer_type}") 
    user.save()
    

