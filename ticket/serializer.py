from rest_framework import serializers
from .models import Problem, Duty


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ["name", "status", "createDate", "author"]

class DutySerializer(serializers.ModelSerializer):
    class Meta:
        model = Duty
        fields = '__all__'