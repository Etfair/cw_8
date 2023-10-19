from django.contrib import admin

from habit.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('owner', 'place', 'time', 'action', 'sign_pleasant_habit', 'related_habit',
                    'period', 'award', 'time_to_complete', 'is_published')
