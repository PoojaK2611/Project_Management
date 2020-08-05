from .models import MyUser, Client, Project
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}


class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['id', 'username']

    # def create(self, validated_data):
    #     validated_data["project"] = self.context.get('request').user
    #     return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True, many=True)
    # user = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id','project_name', 'created_at', 'created_by','user']
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validated_user(self,value):
        return self.context['request'].user.username

    # def create(self, validated_data):
    #     validated_data["user"] = self.context.get('request').user
    #     return super().create(validated_data)
    #
    # def get_user(self, validated_data):
    #     validated_data["user"] = self.context.get('request').user
    #     return super().create(validated_data)
    #     # response = []
    #     # for _user in obj.user.all():
    #     #     user_profile = MyUserSerializer(
    #     #         _user.userprofile,
    #     #         context={'request': self.context['request']})
    #     #     response.append(user_profile.data)
    #     # return response


