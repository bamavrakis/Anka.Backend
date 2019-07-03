from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Teacher, Course, CourseWorker, Student, Attendance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class TeacherSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rut_without_digit = serializers.IntegerField(required=True)
    rut_digit = serializers.CharField(required=True, max_length=16)
    first_name = serializers.CharField(required=True, max_length=128)
    paternal_name = serializers.CharField(required=True, max_length=128)
    maternal_name = serializers.CharField(required=True, max_length=128)
    role = serializers.CharField(required=True, max_length=128)


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=16)
    institution = serializers.CharField(required=True, max_length=100)


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rut_without_digit = serializers.IntegerField(required=True)
    rut_digit = serializers.CharField(required=True, max_length=16)
    first_name = serializers.CharField(required=True, max_length=128)
    paternal_name = serializers.CharField(required=True, max_length=128)
    maternal_name = serializers.CharField(required=True, max_length=128)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'paternal_name',
                  'maternal_name', 'course')


class CourseWorkerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    teacher = serializers.CharField(required=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseWorker
        fields = ('id', 'teacher', 'course', )


class AttendanceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    course = CourseSerializer(read_only=True)
    date = serializers.DateField(required=True)
    student = StudentSerializer(read_only=True)
    status = serializers.BooleanField(required=True)

    class Meta:
        model = Attendance
        fields = ('id', 'course', 'date', 'student', 'status')
