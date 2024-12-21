import logging
from time import sleep
from celery import shared_task
from .models import Job
from website.priority import prioritize_sites

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@shared_task
def task_01(job_id: int):
    TIME_MULTIPLIER = 0.001 # very fast execution per record
    job= Job.objects.get(id=job_id)
    sleep(TIME_MULTIPLIER)
    logger.info(f"Task 01: {job.user.name}'s job id {job.pk} processed ")
    job.status = "completed"
    job.save()
    return True

@shared_task
def task_02(job_id: int):
    TIME_MULTIPLIER = 0.01
    job = Job.objects.get(id=job_id)
    sleep(TIME_MULTIPLIER)
    logger.info(f"Task 02: {job.user.name}'s job id {job.pk} processed ")
    job.status = "completed"
    job.save()
    return True

@shared_task
def task_03(job_id: int):
    TIME_MULTIPLIER = 0.1
    job = Job.objects.get(id=job_id)
    sleep(TIME_MULTIPLIER)
    logger.info(f"Task 03: {job.user.name}'s job id {job.pk} processed ")
    job.status = "completed"
    job.save()
    return True

@shared_task
def task_04(job_id: int):
    TIME_MULTIPLIER = 1
    job = Job.objects.get(id=job_id)
    sleep(TIME_MULTIPLIER)
    logger.info(f"Task 04: {job.user.name}'s job id {job.pk} processed ")
    job.status = "completed"
    job.save()
    return True

@shared_task
def task_05(job_id: int):
    TIME_MULTIPLIER = 10
    job = Job.objects.get(id=job_id)
    sleep(TIME_MULTIPLIER)
    logger.info(f"Task 05: {job.user.name}'s job id {job.pk} processed ")
    job.status = "completed"
    job.save()
    return True


@shared_task
def task_distributer():
    #we have two matrics to consider for the priority score
    #no.of user with "HyperActive" > "VeryActive" > "Active"
    # no. of pending task 01> task 02 > task 03 > task 04 > task 05
    
    sites = prioritize_sites()
    for site in sites:
        if Job.objects.filter(site=site, status="pending").exists():
            pending_jobs = Job.objects.filter(site=site, status="pending")
            for job in pending_jobs:
                if job.task_type == Job.TASK_01:
                    task_01.delay(job.id)
                elif job.task_type == Job.TASK_02:
                    task_02.delay(job.id)
                elif job.task_type == Job.TASK_03:
                    task_03.delay(job.id)
                elif job.task_type == Job.TASK_04:
                    task_04.delay(job.id)
                elif job.task_type == Job.TASK_05:
                    task_05.delay(job.id)
                else:
                    logger.info(f"Task type not found for job id {job.id}")
    return True

    
    