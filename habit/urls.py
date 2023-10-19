from django.urls import path
from rest_framework import routers

from habit.apps import HabitConfig
from habit.views import HabitListAPIView, HabitViewSet

app_name = HabitConfig.name

urlpatterns = [
    path('habit/list/', HabitListAPIView.as_view(), name='public_list'),
]

router = routers.SimpleRouter()
router.register(r'habit', HabitViewSet, basename='habit')


urlpatterns += router.urls
