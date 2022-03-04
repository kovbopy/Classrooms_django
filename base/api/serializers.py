from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from base.models import Classroom, Users


class ClassroomSerializer(ModelSerializer):
    teacher = serializers.StringRelatedField(read_only=True)
    students = serializers.StringRelatedField(read_only=True, many=True)
    subject = serializers.StringRelatedField(read_only=True)
    students_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Classroom
        fields = ["name", "slug", "description", "teacher", "subject",
                'students_count', "students"]


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ["username", "behavior", "password"]

    def validate(self, attrs):
        if Users.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {"username": "User with this name already exists."})
