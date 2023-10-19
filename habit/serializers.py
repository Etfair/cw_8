from rest_framework import serializers

from habit.models import Habit
from habit.validators import HabitValidator


class HabitCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        validator = HabitValidator(data)
        validator(data)

        return data


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
