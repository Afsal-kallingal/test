from rest_framework import serializers
from apps.main.functions import get_auto_id

class BaseModelSerializer(serializers.ModelSerializer):
    auto_id = serializers.CharField(read_only =True)
    creator = serializers.CharField(read_only =True)
    date_added = serializers.CharField(read_only =True)
    def create(self, validated_data):
        validated_data["auto_id"] = get_auto_id(self.Meta.model)
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
    class Meta:
        abstract = True



# class BaseModelSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         auto_id = get_auto_id(self.Meta.model)
#         print(f"Auto ID: {auto_id}")
        
#         validated_data["auto_id"] = auto_id
#         print(f"Validated data before create: {validated_data}")

#         instance = super().create(validated_data)
#         print(f"Created instance: {instance}")

#         return instance

#     class Meta:
#         abstract = True