from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.models import Tracker

from api.serializers import TrackerSerializer

from webapp.models import Project

from api.serializers import ProjectSerializer


class TrackerDetailView(APIView):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer_project = ProjectSerializer(project)
        tracker = Tracker.objects.filter(project_id=pk)
        serializer = TrackerSerializer(tracker, many=True)
        data = {'project': serializer_project.data, 'tracker': serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class TrackerDeleteView(APIView):
    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        tracker = Tracker.objects.filter(project_id=pk)
        tracker.delete()
        project.delete()
        return Response({'pk': pk}, status=status.HTTP_204_NO_CONTENT)


class TrackerUpdateView(APIView):

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        tracker = Tracker.objects.filter(project_id=pk).first()
        serializer_project = ProjectSerializer(project, data=request.data)
        if serializer_project.is_valid():
            serializer_project.save()
        else:
            return Response(serializer_project.errors, status=400)
        serializer = TrackerSerializer(tracker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)




