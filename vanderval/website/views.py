import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.decorators import api_view


#importing the models and serializers
from website.models import Site, UserRecords, Job
from website.serializers import ( SiteSerializer, UserRecordsSerializer, JobSerializer,
                                SiteDetailSerializer, UserRecordsDetailSerializer,
                                JobDetailSerializer)


#importing task distributer
from website.tasks import task_distributer
'''

<Model>ListAPIView> - This view suppport GET and POST request for the model
                    it returns a list of all the objects in the model and
                    you can post a new object or multiple objects to this view.

<Model>OperationAPIView> - This view support GET, PUT and DELETE request for the model/
                        it returns a single object of the model.
                        you can perform actions like update and deletion on the object.

'''


@api_view(['GET'])
def Endpoints(request):
    '''
    a request to this view will return all the endpoints available in this webapp   
    '''
    routes={
        '':'list of endpoints',
        
        'sites/':'[GET,POST]list of all site on this webapp or create single or multiple sites ',
        
        'sites/<site_id>':'[GET,UPDATE,DELETE] specific site',
        
        'user-records/':'[GET,POST] list of all users on this webapp or create single or multiple users',
        
        'user-records/<int:user_records_id>': '[GET,UPDATE,DELETE] specific site',
        
        'jobs/':'[GET,POST] list of all jobs on this webapp or create single or multiple jobs',
        
        'jobs/<int:job_id>/':'[GET,UPDATE,DELETE] specific job'
    }
    return Response(routes)
    

class SiteListAPIView(APIView):
    
    def get(self, request):
        sites = Site.objects.all()
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data)

    def post(self, request):
        with transaction.atomic():
            '''
            with atomicity we are making sure that all object are created or none
            this is done to prevent partial creation of objects and no data inconsistency
            due to replication of data when user try to post again if some error 
            arises
            '''
            serializer = SiteSerializer(data=request.data, many=isinstance(request.data, list))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserRecordsListAPIView(APIView):
   
    def get(self, request):
        user_records = UserRecords.objects.all()
        serializer = UserRecordsSerializer(user_records, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        with transaction.atomic():
            serializer = UserRecordsSerializer(data=request.data, many=isinstance(request.data, list))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class JobListAPIView(APIView):
    
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        with transaction.atomic():
            serializer = JobSerializer(data=request.data, many=isinstance(request.data, list))
            if serializer.is_valid():
                serializer.save()
                #task_distributer.delay() #calling the task distributer
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SiteOperationAPIView(APIView):
    
    def get(self, request, site_id):
        site = Site.objects.get(id=site_id)
        serializer = SiteDetailSerializer(site)
        return Response(serializer.data)

    def put(self, request, site_id):
        site = Site.objects.get(id=site_id)
        data = json.loads(request.body)
        serializer = SiteSerializer(site, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, site_id):
        site = Site.objects.get(id=site_id)
        site.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserRecordsOperationAPIView(APIView):

    def get(self, request, user_records_id):
        user_records = UserRecords.objects.get(id=user_records_id)
        serializer = UserRecordsDetailSerializer(user_records)
        return Response(serializer.data)

    def put(self, request, user_records_id):
        user_records = UserRecords.objects.get(id=user_records_id)
        data = json.loads(request.body)
        serializer = UserRecordsSerializer(user_records, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_records_id):
        user_records = UserRecords.objects.get(id=user_records_id)
        user_records.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobOperationAPIView(APIView):
    
    def get(self, request, job_id):
        job = Job.objects.get(id=job_id)
        serializer = JobDetailSerializer(job)
        return Response(serializer.data)

    def put(self, request, job_id):
        job = Job.objects.get(id=job_id)
        data = json.loads(request.body)
        serializer = JobSerializer(job, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_id):
        job = Job.objects.get(id=job_id)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)