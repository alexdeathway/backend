from rest_framework import serializers
from website.models import Site, UserRecords, Job
from rest_framework.exceptions import ValidationError

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["name", "domain", "url", "description", "record_capicity"]

class UserRecordsSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = UserRecords
        fields = ["name", "site", "email", "phone", "address", "country", "state", "city", "pincode", "dob"]
    

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        #we will be internally assinging the task type and status
        model = Job
        fields = ["user", "site", "execution_time"]


#DETAIL SERIALIZERS ARE FOR THE DETAIL VIEW OF THE MODELS   
#detail serializers with [for future update]nested json data about the related models 
# for example 
# SiteDetailSerializer will return the site details along with the user records
# and UserRecordsDetailSerializer will return the user records along with the jobs

class SiteDetailSerializer(serializers.ModelSerializer):
    user_records = UserRecordsSerializer(many=True)
    class Meta:
        model = Site
        fields = ["name", "domain", "url", "description", "record_capicity", "user_records", "total_users", "total_jobs"]

class UserRecordsDetailSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True)
    class Meta:
        model = UserRecords
        fields = ["site", "name", "email", "phone", "address", "country", "state", "city", "pincode", "dob"]

class JobDetailSerializer(serializers.ModelSerializer):
    user=serializers.CharField(source='user.name', read_only=True)
    site=serializers.CharField(source='site.name', read_only=True)
    class Meta:
        model = Job
        fields = ["user", "site", "execution_time","task_type", "status"]