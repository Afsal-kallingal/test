from django.conf import settings
from django.urls import path
from django.urls import path
from apps.project.api_v1.views import *
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("project",ProjectViewSet,basename='project-viewset'),
router.register("tudo",TudoViewSet,basename='tudo'),



urlpatterns = [
    # path("investors/", InvestorListCreateAPIView.as_view(), name="investor-list-create"),
]

app_name = "api_v1"
urlpatterns += router.urls
