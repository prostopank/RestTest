from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from task.models import Task
from task.serializers import CreateAssignTaskSerializer, CompleteTaskSerializer, ListTaskSerializers
from user.models import User


class CreateTaskViewSet(generics.CreateAPIView):
    serializer_class = CreateAssignTaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()


@extend_schema(methods=['PATCH'], exclude=True)
class AssignTaskViewSet(generics.UpdateAPIView):
    serializer_class = CreateAssignTaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()


@extend_schema(methods=['PATCH'], exclude=True)
class CompleteTaskViewSet(generics.UpdateAPIView):
    serializer_class = CompleteTaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()


class ListTaskViewSet(generics.ListAPIView):
    serializer_class = ListTaskSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = []
        if user.type == User.CUSTOMER:
            queryset = Task.objects.filter(customer=user)
        elif user.type == User.EMPLOYEE:
            queryset = Task.objects.filter(Q(status=Task.WAITING_FOR_THE_EMPLOYEE) | Q(employee=user))
        return queryset
