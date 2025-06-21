from celery import shared_task, Celery
from celery.schedules import crontab
from toolnest_backend.celery import app  # type: Celery
from datetime import timedelta
from django.utils import timezone
from .models.enums import WEEKDAY_MAP
from .models.models import DailyTask, TaskInstance


@shared_task
def generate_task_instances_for_week(daily_task_id):
    try:
        task = DailyTask.objects.get(id=daily_task_id)
    except DailyTask.DoesNotExist:
        return "DailyTask not found."

    if not task.is_active:
        return "Task is inactive. Skipping instance creation."

    today = timezone.localdate()
    created = 0

    for offset in range(7):
        future_date = today + timedelta(days=offset)
        weekday = WEEKDAY_MAP[future_date.weekday()]

        if weekday in task.weekdays:
            _, created_obj = TaskInstance.objects.get_or_create(
                parent_daily_task=task,
                user=task.user,
                date=future_date,
                defaults={
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority,
                },
            )
            if created_obj:
                created += 1

    return f"Created {created} task instances for DailyTask: {task.title}"


@shared_task
def generate_task_instances_for_today():
    today = timezone.localdate()
    weekday = WEEKDAY_MAP[today.weekday()]
    count = 0

    for task in DailyTask.objects.filter(is_active=True, weekdays__contains=[weekday]):
        _, created = TaskInstance.objects.get_or_create(
            parent_daily_task=task,
            user=task.user,
            date=today,
            defaults={
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
            },
        )
        if created:
            count += 1

    return f"Generated {count} task instances for today"


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=4, minute=0),
        generate_task_instances_for_today(),
        name="Generate daily task instances",
    )
