from django.db import models


class Weekday(models.TextChoices):
    MONDAY = "mon", "Monday"
    TUESDAY = "tue", "Tuesday"
    WEDNESDAY = "wed", "Wednesday"
    THURSDAY = "thu", "Thursday"
    FRIDAY = "fri", "Friday"
    SATURDAY = "sat", "Saturday"
    SUNDAY = "sun", "Sunday"


WEEKDAY_MAP = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}
