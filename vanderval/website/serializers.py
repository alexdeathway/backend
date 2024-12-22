from rest_framework import serializers
from website.models import Site, UserRecords, Job
from rest_framework.exceptions import ValidationError

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["name", "domain", "url", "description", "record_capicity"]

class UserRecordsSerializer(serializers.ModelSerializer): 
    
    #add option to retrive the site field by name.
    #site=serializers.CharField(source='site.name', read_only=True)
    
    class Meta:
        model = UserRecords
        fields = ["name", "site", "email", "phone", "address", "country", "state", "city", "pincode", "dob"]
    
    #removing this as we are reverting to the default behaviour
    #might use for feature updates 

    # def create(self, validated_data):
    #     site_instance = validated_data.get('site') 
    #     if not site_instance:
    #         raise ValidationError("Site is required.")

    #     # Now create the UserRecords object
    #     user_record = UserRecords.objects.create(**validated_data)

    #     return user_record

    # def update(self, instance, validated_data):
    #     site_instance = validated_data.get('site')
    #     if site_instance:
    #         instance.site = site_instance  

       
    #     for attr, value in validated_data.items():
    #         if attr != 'site': 
    #             setattr(instance, attr, value)
        
    #     instance.save()
    #     return instance
    

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        #we will be internally assinging the task type and status
        model = Job
        fields = ["user", "site", "execution_time"]


#detail serializers nested json data about the related models for example 
# SiteDetailSerializer will return the site details along with the user records
# and UserRecordsDetailSerializer will return the user records along with the jobs

class SiteDetailSerializer(serializers.ModelSerializer):
    user_records = UserRecordsSerializer(many=True)
    class Meta:
        model = Site
        fields = ["name", "domain", "url", "description", "record_capicity", "user_records"]

class UserRecordsDetailSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True)
    class Meta:
        model = UserRecords
        fields = ["site", "name", "email", "phone", "address", "country", "state", "city", "pincode", "dob","customer_type", "jobs"]

class JobDetailSerializer(serializers.ModelSerializer):
    user=serializers.CharField(source='user.name', read_only=True)
    site=serializers.CharField(source='site.name', read_only=True)
    class Meta:
        model = Job
        fields = ["user", "site", "execution_time","task_type", "status"]