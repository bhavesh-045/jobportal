from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from django.shortcuts import get_object_or_404
from .forms import JobPostForm
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

@api_view(['GET'])
def job_list_view(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def job_detail(request,id):
    job = get_object_or_404(Job,id=id)
    serializer = JobSerializer(job)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def job_create1(request):
    if request.user.role != 'recruiter':
        return Response({
            'error':'Only recruiter can post jobs '
        },status=status.HTTP_403_FORBIDDEN)
    
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        job = serializer.save()
        job.posted_by = request.user
        job.save()
        return Response(JobSerializer(job).data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def job_update(request,id):
    try: 
            job = Job.objects.get(id=id,posted_by=request.user)
    except Job.DoesNotExist:
         return Response({"error": "Not allowed or Job not Found"},status=status.HTTP_403_FORBIDDEN)
    
    serializer = JobSerializer(job,data=request.data)
    if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def job_delete(request,id):
    try: 
        job = Job.objects.get(id=id,posted_by=request.user)
    except Job.DoesNotExist:
         return Response({"error": "Not allowed or Job not Found"},status=status.HTTP_403_FORBIDDEN)
    job.delete()
    return Response({"message":"Job Deleted Successfully"})