from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from website.models import Job, UserRecords
from django.db import transaction


@receiver(post_save, sender=Job)
def update_total_job_in_site(sender, instance, created, **kwargs):
    '''
    this update the total job in the site
    '''
    site= instance.site
    #instead of doing +=1 we are doing a count to get the total jobs because there
    #are some job already in database and this new signal is due to requirement 
    #change.(checkout PR#1 for more deatils)
    total_job = Job.objects.filter(site=site).count()
    site.total_jobs = total_job
    site.save()

@receiver(post_save, sender=UserRecords)
def update_total_user_in_site(sender, instance, created, **kwargs):
    '''
    this update the total user in the site
    '''
    site= instance.site
    total_user = UserRecords.objects.filter(site=site).count()
    site.total_users = total_user
    site.save()
   