from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    detail_serializer_class = UserDetailSerializer
    filterset_fields = ['name', 'role__name']

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend, )

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class

        return super(UserViewSet, self).get_serializer_class()


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer


class WatchTypeViewSet(viewsets.ModelViewSet):
    queryset = WatchType.objects.all()
    serializer_class = WatchTypeSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    detail_serializer_class = TaskDetailSerializer
    filterset_fields = ['name', 'work_type__uid', 'work_type__name',
                        'worker__name', 'worker__role', 'worker__uid',
                        'progress__uid', 'progress__name']

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend, )

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class

        return super(UserViewSet, self).get_serializer_class()


class WatchViewSet(viewsets.ModelViewSet):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    detail_serializer_class = WatchDetailSerializer
    filterset_fields = ['date', 'watch_type']

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend, )

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class

        return super(UserViewSet, self).get_serializer_class()