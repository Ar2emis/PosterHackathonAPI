from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import base64
from rest_framework.decorators import action
from django.core.files.base import ContentFile
import random
import string


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

    @action(detail=True, methods=['get'])
    def set_active(self, request, pk=None):
        user = self.get_object()

        is_active = None
        
        parameter = request.query_params.get('active', None)
        
        if parameter == 'true':
            is_active = True
        elif parameter == 'false':
            is_active = False
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user.active = is_active
        user.save()

        data = self.get_serializer_class()(user, context={'request': request}).data

        return Response(data=data, status=status.HTTP_200_OK)


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
    image_serializer_class = ImageSerializer
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
        elif self.action == 'upload_image':
            if hasattr(self, 'detail_serializer_class'):
                return self.image_serializer_class

        return super(TaskViewSet, self).get_serializer_class()

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        images = []
        for index in range(len(queryset)):
            print(queryset[index])
            if not queryset[index].image:
                images.append(None)
            else:
                images.append(queryset[index].image.path)

        images_data = []
        for index in range(len(images)):
            if images[index] == None:
                images_data.append(None)
            else:
                with open(images[index], "rb") as img_file:
                    image_data = base64.b64encode(img_file.read())
                    images_data.append(image_data)
                
        serializer = self.get_serializer_class()

        data = serializer(queryset, many=True, context={'request': request}).data

        for index in range(len(data)):
            data[index]['image'] = images_data[index]
           
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        task = queryset.filter(pk=pk).first()

        if task == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        image_data = None

        if task.image:
            with open(task.image.path, "rb") as img_file:
                    image_data = base64.b64encode(img_file.read())

        data = self.get_serializer().to_representation(task)

        data['image'] = image_data

        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def upload_image(self, request, pk=None):
        task = self.get_object()

        serializer = self.get_serializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        image_data = serializer.data['image']

        image = ContentFile(base64.b64decode(image_data))

        filename = ''.join(random.choices(string.ascii_letters +
                             string.digits, k = 10)) + '.jpg'

        task.image.save(filename, image, save=True)

        task.save()

        data = TaskDetailSerializer(task, context={'request': request}).data

        data['image'] = image_data

        return Response(data=data, status=status.HTTP_200_OK)


class WatchViewSet(viewsets.ModelViewSet):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    detail_serializer_class = WatchDetailSerializer
    add_task_serializer_class = TaskSerializer
    filterset_fields = ['date', 'watch_type__name']

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend, )

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class

        if self.action == 'add_task':
            if hasattr(self, 'add_task_serializer_class'):
                return self.add_task_serializer_class

        return super(WatchViewSet, self).get_serializer_class()

    @action(detail=True, methods=['post'])
    def add_task(self, request, pk=None):
        watch = self.get_object()

        serializer = self.get_serializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        task = serializer.instance

        task.save()

        watch.tasks.add(task)

        watch.save()

        data = WatchDetailSerializer(watch, context={'request': request}).data

        return Response(data=data, status=status.HTTP_200_OK)