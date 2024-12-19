from rest_framework import serializers
from website.models import Site, UserRecords, Job


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["name", "domain", "url", "description", "record_capicity"]

class UserRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecords
        fields = ["site", "name", "email", "phone", "address", "country", "state", "city", "pincode", "dob"]

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["user", "site", "execution_time"]