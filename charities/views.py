from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task
from charities.serializers import (
    TaskSerializer, CharitySerializer, BenefactorSerializer
)

class BenefactorRegistration(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request):
        benefactor_serializer = BenefactorSerializer(data = request.data)
        if benefactor_serializer.is_valid():
            benefactor_serializer.save(user = request.user)
            return Response({"message" : "benefactor added"})
        return Response({"message": benefactor_serializer.errors})


class CharityRegistration(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request):
        charity_serializer = CharitySerializer(data = request.data)
        if charity_serializer.is_valid():
            charity_serializer.save(user = request.user)
            return Response({"message" : "charity added"})
        return Response({"message": charity_serializer.errors})


class Tasks(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all_related_tasks_to_user(self.request.user)

    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            "charity_id": request.user.charity.id
        }
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsCharityOwner, ]

        return [permission() for permission in self.permission_classes]

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Task.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param
        exclude_lookups = {}
        for name, value in Task.excluding_lookups:
            param = self.request.GET.get(value)
            if param:
                exclude_lookups[name] = param

        return queryset.filter(**filter_lookups).exclude(**exclude_lookups)


class TaskRequest(APIView):
    permission_classes = [IsBenefactor]

    def get(self , request , task_id):
        task = get_object_or_404(Task , pk = task_id)
        if task.state != Task.TaskStatus.PENDING:
            return Response(data={'detail': 'This task is not pending.'} , status=404)
        task.assign_to_benefactor(request.user.benefactor)
        return Response(data={'detail': 'Request sent.'} , status=200) 


class TaskResponse(APIView):
    permission_classes = [ IsCharityOwner]

    def post(self , request , task_id):
        task = get_object_or_404(Task , pk = task_id)
        if request.data["response"] != "A" and request.data["response"] != "R":
            return Response(data={'detail': 'Required field ("A" for accepted / "R" for rejected)'} , status= 400)
        elif task.state != Task.TaskStatus.WAITING:
            return Response(data={'detail': 'This task is not waiting.'} , status=404)
        elif request.data["response"] == "A":
            task.response_to_benefactor_request(request.data["response"]) 
            return Response(data={'detail': 'Response sent.'} , status=200)

        elif request.data["response"] == "R":
            task.response_to_benefactor_request(request.data["response"])
            return Response(data={'detail': 'Response sent.'} , status=200)


class DoneTask(APIView):
    permission_classes = [IsCharityOwner]
    def post(self , request , task_id):
        task = get_object_or_404(Task , pk = task_id)
        if task.state != Task.TaskStatus.ASSIGNED:
            return Response(data={'detail': 'Task is not assigned yet.'} , status=404)
        else:
            task.done()
            return Response(data={'detail': 'Task has been done successfully.'} , status=200)