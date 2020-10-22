from django.forms import widgets
from rest_framework import serializers


class SnippetSerializer(serializers.Serializer):
    code = serializers.CharField(widget=widgets.Textarea, max_length=100000, required=True)
    title = serializers.CharField(required=False, max_length=100)
