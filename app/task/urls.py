from django.urls import path

from task.views import CreateTaskViewSet, AssignTaskViewSet, CompleteTaskViewSet, ListTaskViewSet

urlpatterns = [
    path('create/', CreateTaskViewSet.as_view(), name='task_create'),
    path('assign/<int:pk>/', AssignTaskViewSet.as_view(), name='task_assign'),
    path('complete/<int:pk>/', CompleteTaskViewSet.as_view(), name='task_complete'),
    path('list/', ListTaskViewSet.as_view(), name='task_list'),
]
