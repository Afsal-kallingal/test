from apps.main.serializers import BaseModelSerializer
from rest_framework import serializers
from apps.project.models import *
from apps.user_account.functions import validate_phone
from apps.user_account.models import User



class TodoSerializer(BaseModelSerializer):
    class Meta:
        model = Tudo
        fields = '__all__'

class ProjectSerializer(BaseModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'