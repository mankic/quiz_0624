from rest_framework import serializers

# from user.models import User as UserModel
from post.models import Company as CompanyModel
from post.models import JobPost as JobPostModel
from post.models import JobType as JobTypeModel
from post.models import SkillSet as SkillSetModel
from post.models import JobPostSkillSet as JobPostSkillSetModel

class CompanySerializer(serializers.ModelSerializer):
                
    class Meta:
        model = CompanyModel
        fields = ["company_name", "business_area"]


class JobTypeSerializer(serializers.ModelSerializer):
                
    class Meta:
        model = JobTypeModel
        fields = ["job_type"]


class JobPostSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    # job_type = JobTypeSerializer()
    skillset = serializers.SerializerMethodField()

    def get_skillset(self, obj):
        skillsets = obj.skillset_set.all()
        skillset_names = [skillset.name for skillset in skillsets]
        return skillset_names

    class Meta:
        model = JobPostModel
        fields = ["job_type", "company", "job_description", "salary", "skillset"]


class SkillSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillSetModel
        fields = ["name", "job_posts"]


class JobPostSkillSetSerializer(serializers.ModelSerializer):
    skill_set = SkillSetSerializer()
    job_post = JobPostSerializer()
    class Meta:
        model = JobPostSkillSetModel
        fields = ["skill_set", "job_post"]