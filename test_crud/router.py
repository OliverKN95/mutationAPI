from django.urls import path
from django.db import router
from test_crud.views import getStadisticsViewset, hasMutationViewset
from rest_framework import routers

app_name = 'test'

router = routers.SimpleRouter()


urlpatterns = [
    path('mutation/', hasMutationViewset.as_view()),
    path('stats/', getStadisticsViewset.as_view()),
]

urlpatterns = router.urls + urlpatterns