from django.db import models


# Create your models here.
class Site(models.Model):
    RECORD_CAPACITY_LOW = 1  # user records between 500-10000
    RECORD_CAPACITY_MEDIUM = 2  # user records between 10000-50000
    RECORD_CAPACITY_HIGH = 3  # user records between 50000-200000

    RECORD_CAPACITY_CHOICES = (
        (RECORD_CAPACITY_LOW, "Low"),
        (RECORD_CAPACITY_MEDIUM, "Medium"),
        (RECORD_CAPACITY_HIGH, "High"),
    )

    name = models.CharField(max_length=100)
    domain = models.URLField()
    url = models.URLField()
    description = models.TextField()
    record_capicity = models.IntegerField(choices=RECORD_CAPACITY_CHOICES)

    def __str__(self):
        return self.name

# you can choose to reuse the User model from django.contrib.auth.models
class UserRecords(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="user_records")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    dob = models.DateField()
    is_active = models.BooleanField(default=True)  # Do not count for active records if False
    customer_type = models.CharField(max_length=20, blank=True)

    def _calculate_customer_type(self):
        """
        objective 2[in readme]: Determine customer type based on job count.
        we will be priotizing the customer based on the number of jobs they have.
        like hyperactive will be given more priority than all other types.
        """
        job_count = Job.objects.filter(user=self, status='pending').count()
        if job_count < 5:
            return "Active"
        elif job_count < 10:
            return "VeryActive"
        return "HyperActive"
    

    def save(self, *args, **kwargs):
        self.customer_type = "Active"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Job(models.Model):
    '''
    job model
    '''
    TASK_01 = 'task_01'
    TASK_02 = 'task_02'
    TASK_03 = 'task_03'
    TASK_04 = 'task_04'
    TASK_05 = 'task_05'

    TASK_CHOICES = (
        (TASK_01, 'Task 01'),
        (TASK_02, 'Task 02'),
        (TASK_03, 'Task 03'),
        (TASK_04, 'Task 04'),
        (TASK_05, 'Task 05'),
    )
    user = models.ForeignKey(UserRecords, on_delete=models.CASCADE,related_name="jobs")
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    execution_time = models.FloatField()
    task_type = models.CharField(max_length=10, choices=TASK_CHOICES, blank=True)
    status = models.CharField(max_length=10, default='pending')


    def save(self, *args, **kwargs):
        '''
        we will need a validation for this field. as only task with
        execution time of 0.001, 0.01, 0.1, 1, 10 seconds and below will be considered
        valid

        '''
        
        if self.execution_time <= 0.001:
            self.task_type = self.TASK_01
        elif self.execution_time <= 0.01:
            self.task_type = self.TASK_02
        elif self.execution_time <= 0.1:
            self.task_type = self.TASK_03
        elif self.execution_time <= 1:
            self.task_type = self.TASK_04
        elif self.execution_time <= 10:
            self.task_type = self.TASK_05
        else:
            self.status = "failed"

        
        
        #updating the customer type of the user record 
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.name} -{self.pk}- {self.task_type}"

