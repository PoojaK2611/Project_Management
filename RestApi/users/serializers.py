from .models import MyUser, Client, Project
from rest_framework import serializers


class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['id', 'username']


class ProjectSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True, many=True)
    created_by = serializers.StringRelatedField( read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at', 'created_by','user']
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def get_value(self, dictionary):
        dictionary["user"] = self.context.get('request').user
        return super().get_value(dictionary)


class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField( read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}


