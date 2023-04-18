from rest_framework import serializers

from webapp.models import Tracker

from webapp.models import Project


class TrackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tracker
        fields = ['id', 'summary', 'description', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'start_date', 'end_date']
