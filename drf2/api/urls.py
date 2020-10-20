from django.conf.urls import url
from api import views

urlpatterns = [
    url('snippets/', views.SnippetList.as_view()),
    url('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]
