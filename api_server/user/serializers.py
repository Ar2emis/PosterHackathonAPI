from rest_framework import serializers
from .models import *
from drf_extra_fields.fields import HybridImageField




class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ['url', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.HyperlinkedRelatedField(view_name='role-detail', queryset=Role.objects.all())

    class Meta:
        model = User
        fields = ['url', 'name', 'role', 'active']


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ['url', 'name', 'role', 'active']


class ProgressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Progress
        fields = ['url', 'name']


class WatchTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WatchType
        fields = ['url', 'name']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    worker = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset=User.objects.all(), required=False)
    progress = serializers.HyperlinkedRelatedField(view_name='progress-detail', queryset=Progress.objects.all(), required=False)
    work_type = serializers.HyperlinkedRelatedField(view_name='role-detail', queryset=Role.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ['url', 'name', 'text', 'worker', 'image', 'progress', 'work_type']


class TaskDetailSerializer(serializers.HyperlinkedModelSerializer):
    worker = UserDetailSerializer()
    progress = ProgressSerializer()
    work_type = RoleSerializer()

    class Meta:
        model = Task
        fields = ['url', 'name', 'text', 'worker', 'image', 'progress', 'work_type']


class ImageSerializer(serializers.Serializer):
    image = serializers.CharField()

    class Meta:
        fields = ['image']

class WatchSerializer(serializers.HyperlinkedModelSerializer):
    watch_type = serializers.HyperlinkedRelatedField(view_name='watchtype-detail', queryset=WatchType.objects.all())
    tasks = serializers.HyperlinkedRelatedField(view_name='task-detail', many=True, queryset=Task.objects.all(), required=False)

    class Meta:
        model = Watch
        fields = ['url', 'date', 'watch_type', 'tasks']


class WatchDetailSerializer(serializers.HyperlinkedModelSerializer):
    watch_type = WatchTypeSerializer()
    tasks = TaskDetailSerializer(many=True)

    class Meta:
        model = Watch
        fields = ['url', 'date', 'watch_type', 'tasks']