from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from post.serializers import JobPostSerializer
from .models import (
    JobPostSkillSet,
    JobType,
    JobPost,
    Company,
    SkillSet
)
from django.db.models.query_utils import Q


class SkillView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skills = self.request.query_params.getlist('skills', '')
        print("skills = ", end=""), print(skills)

        query = Q(skill_set_id=3) | Q(skill_set_id=2)

        jobpostskillset_objs = JobPostSkillSet.objects.filter(query)
        jobpost_ids = [jobpostskillset_obj.job_post_id for jobpostskillset_obj in jobpostskillset_objs]
        
        jobpost_objs = [JobPost.objects.get(id=jobpost_id) for jobpost_id in jobpost_ids]
       
        return Response(JobPostSerializer(jobpost_objs, many=True).data, status=status.HTTP_200_OK)


class JobView(APIView):

    def post(self, request):
        job_type = int( request.data.get("job_type", None) )
        company_name = request.data.get("company_name", None)
     
        job_type_table = JobType.objects.filter(id=job_type)
        # print(job_type_table)
        company_get_create = Company.objects.get_or_create(company_name=company_name)
        # print(type(company_get_create)) => <class 'tuple'>     # (<Company: Company object (14)>, True)
        company_obj = company_get_create[0]  
        # print(company_obj)
        # print(type(company_obj))
        
        if not job_type_table.exists():
            return Response({"massage":"job type 이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # if not company.exists():
        #     company = Company(company_name=company_name).save()
        # else:
        #     company = company.first()

        job_serializer = JobPostSerializer(data=request.data)
        if job_serializer.is_valid():
            job_serializer.save(company=company_obj)
            return Response({"message":"저장완료!!"}, status=status.HTTP_200_OK)

        return Response(job_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


