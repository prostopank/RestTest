from django.db import models
from django.utils import timezone

from user.models import User


class Task(models.Model):
    WAITING_FOR_THE_EMPLOYEE = 'WFTE'
    IN_PROGRESS = 'INPR'
    COMPLETED = 'COMP'
    TASK_STATUS = {
        WAITING_FOR_THE_EMPLOYEE: 'Waiting for the employee',
        IN_PROGRESS: 'In progress',
        COMPLETED: 'Completed',
    }
    name = models.CharField(max_length=100, null=False, blank=False)
    customer = models.ForeignKey(User, related_name='customer', on_delete=models.PROTECT)
    employee = models.ForeignKey(User, related_name='employee', on_delete=models.PROTECT, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    finished_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=4, choices=TASK_STATUS, default=WAITING_FOR_THE_EMPLOYEE)
    report = models.TextField()

    class Meta:
        permissions = [
            ("assign_task", "Can assign the tasks"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can completed a task by setting its status as completed"),
        ]
