from django.utils import timezone
from rest_framework import serializers

from task.models import Task


class CreateAssignTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name']
        extra_kwargs = {'name': {'required': False}}

    def create(self, validated_data):
        user = self.context['request'].user
        if user.type == user.EMPLOYEE:
            raise serializers.ValidationError("User type must be Customer")
        task = Task.objects.create(
            name=validated_data['name'],
            customer=user,
        )
        task.save()

        return task

    def update(self, instance, validated_data):
        if instance.employee:
            raise serializers.ValidationError("Task already in progress")
        user = self.context['request'].user
        if user.type == user.CUSTOMER:
            raise serializers.ValidationError("User type must be Employee")
        instance.employee = user
        instance.status = Task.IN_PROGRESS
        instance.save()
        return instance


class CompleteTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['report']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.type == user.CUSTOMER:
            raise serializers.ValidationError("User type must be Employee")
        elif instance.employee != user:
            raise serializers.ValidationError("Wrong employee")
        elif instance.status == Task.COMPLETED:
            raise serializers.ValidationError("Task already completed")
        instance.report = validated_data['report']
        instance.finished_date = timezone.now()
        instance.status = Task.COMPLETED
        instance.save()
        return instance


class ListTaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'customer', 'employee', 'created_date', 'finished_date', 'status', 'report']
