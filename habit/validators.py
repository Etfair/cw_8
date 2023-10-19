from django.core.exceptions import ValidationError


class HabitValidator:

    def __init__(self, data: dict):
        self.related_habit = data.get('related_habit')
        self.sign_pleasant_habit = data.get('sign_pleasant_habit')
        self.award = data.get('award')

    def __call__(self, value):
        if self.sign_pleasant_habit and (self.related_habit or self.award):
            """Проверка, что у приятной привычки не может быть указана связанная привычка и награда"""
            raise ValidationError(
                {"related_habit": "Приятная привычка не может иметь связанной привычки или вознаграждения.",
                 "award": "Вознаграждение не может быть указано для приятной привычки."})

        if self.related_habit and self.award:
            """Проверка, что нельзя указать связанную привычку и вознаграждение"""
            raise ValidationError('Вы не можете выбирать связанную привычку и вознаграждение одновременно')

        if self.sign_pleasant_habit and not self.related_habit:
            """ Проверка, что в связанной привычке есть признак приятной привычки"""
            raise ValidationError("В связанной привычке отсутствует признак приятной привычки")

        elif not self.sign_pleasant_habit and not (self.related_habit or self.award):
            raise ValidationError({"Поле должно быть заполнено."})
