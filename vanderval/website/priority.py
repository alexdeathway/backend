from .models import Site, Job
from django.db.models import Count


'''
[updated as per discussion on PR#1] objective 4 [in readme]
we are here creating a function that will calculate the priority score for the site
on the basis of the following metrics:

1. no of active users in the site that is RECORD_CAPACITY_LOW, RECORD_CAPACITY_MEDIUM, RECORD_CAPACITY_HIGH
2.type of job in the site(execution time).

'''
from .models import Site, Job
from django.db.models import Count

def get_priority_score(site):
    """
    Calculate priority score for the site based on the given metrics:
    1. Record capacity: High > Medium > Low
    2. Pending tasks: task_01 > task_02 > task_03 > task_04 > task_05
    """
    # Record capacity priority weights
    record_capacity_weights = {
        Site.RECORD_CAPACITY_HIGH: 3,
        Site.RECORD_CAPACITY_MEDIUM: 2,
        Site.RECORD_CAPACITY_LOW: 1,
    }

    
    record_capacity_score = record_capacity_weights.get(site.record_capicity, 0)

    
    task_priority_weights = {
        "task_01": 5,
        "task_02": 4,
        "task_03": 3,
        "task_04": 2,
        "task_05": 1,
    }

   
    task_counts = Job.objects.filter(site=site, status="pending").values("task_type").annotate(
        count=Count("id")
    )

    task_priority_score = sum(
        task_priority_weights[task["task_type"]] * task["count"]
        for task in task_counts
        if task["task_type"] in task_priority_weights
    )

    total_priority_score = record_capacity_score + task_priority_score
    return total_priority_score

def prioritize_sites():
    """
    Get all sites sorted by priority score in descending order.
    """
    sites = Site.objects.all()
    sites_with_priority = sorted(sites, key=lambda site: get_priority_score(site), reverse=True)
    return sites_with_priority
