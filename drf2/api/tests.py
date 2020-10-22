from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers

from api.models import Snippet
from api.serializers import SnippetSerializer


class Tests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.title = 'title'
        self.code = 'required123code'
        self.snippet_with_required = Snippet.objects.create(title=self.title, code=self.code)
        self.snippet_without_required = Snippet.objects.create(title=self.title)

    def test_serializer_with_required_field(self):
        # for deserialization is valid as the required fields are present
        serializer = SnippetSerializer(data={'code': self.code, 'title': self.title})
        self.assertTrue(serializer.is_valid())
        # for serialization is valid as well
        serializer = SnippetSerializer({'code': self.code, 'title': self.title})
        result = serializer.data
        self.assertEquals(
            result,
            serializers.SortedDictWithMetadata({'code': self.code, 'title': self.title})
        )

    def test_serializer_without_required_field(self):
        # for deserialization is not valid and will fail due to 'code' is not present
        serializer = SnippetSerializer(data={'title': self.title})
        self.assertFalse(serializer.is_valid())
        # for serialization is valid despite the data doesn't have the required field 'code'
        serializer = SnippetSerializer({'title': self.title})
        result = serializer.data
        self.assertEquals(
            result,
            serializers.SortedDictWithMetadata({'title': self.title, 'code': None})
        )

    def test_api_get(self):
        # in order to test all the flow, we check that happens the same with objects without
        # required serializer fields
        response = self.client.get('/snippets/')
        json_response = JSONRenderer().render(response.data)
        self.assertEquals(
            json_response,
            '[{"code": "required123code", "title": "title"}, {"code": "", "title": "title"}]'
        )
