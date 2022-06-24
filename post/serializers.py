from rest_framework import serializers

# from user.models import User as UserModel
from post.models import Company as CompanyModel
from post.models import JobPost as JobPostModel
from post.models import JobPostSkillSet as JobPostSkillSetModel

class CompanySerializer(serializers.ModelSerializer):
                
    class Meta:
        model = CompanyModel
        fields = ["company_name", "business_area"]


class JobPostSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = JobPostModel
        fields = ["job_type", "company","job_description","salary"]


class JobPostSkillSetSerializer(serializers.ModelSerializer):
    job_post = JobPostSerializer()
    class Meta:
        model = JobPostSkillSetModel
        fields = ["skill_set", "job_post"]