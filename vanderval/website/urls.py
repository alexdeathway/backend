from django.urls import path
from website.views import (
                SiteListAPIView, SiteOperationAPIView,
                UserRecordsListAPIView, UserRecordsOperationAPIView,
                JobListAPIView, JobOperationAPIView  
                )

urlpatterns = [
    path('',),
    path('sites/', SiteListAPIView.as_view(), name='site-list'),
    path('sites/<int:site_id>/', SiteOperationAPIView.as_view(), name='site-operation'),
    path('user-records/', UserRecordsListAPIView.as_view(), name='user-records-list'),
    path('user-records/<int:user_records_id>/', UserRecordsOperationAPIView.as_view(), name='user-records-operation'),
    path('jobs/', JobListAPIView.as_view(), name='job-list'),
    path('jobs/<int:job_id>/', JobOperationAPIView.as_view(), name='job-operation'),
]