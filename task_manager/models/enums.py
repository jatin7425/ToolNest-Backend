from django.db import models


class Weekday(models.TextChoices):
    MONDAY = "mon", "Monday"
    TUESDAY = "tue", "Tuesday"
    WEDNESDAY = "wed", "Wednesday"
    THURSDAY = "thu", "Thursday"
    FRIDAY = "fri", "Friday"
    SATURDAY = "sat", "Saturday"
    SUNDAY = "sun", "Sunday"
