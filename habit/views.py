from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from habit.tasks import create_periodic_task
from habit.models import Habit
from habit.paginators import HabitPaginator
from habit.serializers import HabitSerializer, HabitCreateSerializer


class HabitViewSet(viewsets.ModelViewSet):
    pagination_class = HabitPaginator
    serializer_class = HabitCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        new_habit = serializer.save()
        create_periodic_task.delay(new_habit.id)


class HabitListAPIView(generics.ListAPIView):
    pagination_class = HabitPaginator
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]
