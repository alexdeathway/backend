from .models import Site, Job
from django.db.models import Count


'''
objective 4 [in readme]
we are here creating a function that will calculate the priority score for the site
on tthe basis of the level of activity of users and the pending tasks.
'''

def get_priority_score(site):
    """
    Calculate priority score for the site based on the given metrics.
    Higher scores indicate higher priority.
    """
    # User priorities: "HyperActive" > "VeryActive" > "Active"
    user_priority_weights = {
        "HyperActive": 3,
        "VeryActive": 2,
        "Active": 1,
    }

    user_counts = site.user_records.filter(is_active=True).values("customer_type").annotate(
        count=Count("id")
    )

    user_priority_score = sum(
        user_priority_weights[user["customer_type"]] * user["count"]
        for user in user_counts
        if user["customer_type"] in user_priority_weights
    )

   
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
    total_priority_score = user_priority_score + task_priority_score
    return total_priority_score

def prioritize_sites():
    """
    Get all sites sorted by priority score in descending order.
    we will use this list to pass the site to the task_distributer
    """
    sites = Site.objects.all()
    sites_with_priority = sorted(sites, key=lambda site: get_priority_score(site), reverse=True)
    return sites_with_priority
