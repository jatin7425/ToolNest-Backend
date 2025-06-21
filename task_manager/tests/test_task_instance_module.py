import pytest
from django.urls import reverse
from django.utils import timezone
from task_manager.models.enums import WEEKDAY_MAP
from task_manager.models.models import DailyTask, TaskInstance
from task_manager.tasks import generate_task_instances_for_week


@pytest.mark.django_db
def test_task_instance_created_from_active_daily_task(user):
    today = timezone.localtime().date()
    daily_task = DailyTask.objects.create(
        user=user,
        title="Auto Generate",
        weekdays=["mon", "tue", "wed", "thu", "fri", "sat", "sun"],  # all days
        is_active=True,
    )

    generate_task_instances_for_week(daily_task.id)

    assert TaskInstance.objects.count() == 7  # One for each day
    today_instance = TaskInstance.objects.filter(date=today).first()
    assert today_instance.title == "Auto Generate"
    assert today_instance.user == user


@pytest.mark.django_db
def test_duplicate_task_instance_not_created(user):
    today = timezone.localtime().date()
    daily_task = DailyTask.objects.create(
        user=user,
        title="No Duplicate",
        weekdays=[WEEKDAY_MAP[today.weekday()]],
        is_active=True,
    )
    TaskInstance.objects.create(
        parent_daily_task=daily_task,
        user=user,
        title=daily_task.title,
        description=daily_task.description,
        priority=daily_task.priority,
        date=today,
    )

    generate_task_instances_for_week(daily_task.id)

    assert TaskInstance.objects.count() == 1  # No duplicate


@pytest.mark.django_db
def test_inactive_daily_task_skipped(user):
    today = timezone.localtime().date()
    daily_task = DailyTask.objects.create(
        user=user,
        title="Skip Me",
        weekdays=[WEEKDAY_MAP[today.weekday()]],
        is_active=False,  # Inactive
    )

    generate_task_instances_for_week(daily_task.id)

    assert TaskInstance.objects.count() == 0


@pytest.mark.django_db
def test_wrong_weekday_skipped(user):
    # Set a weekday that's NOT today
    today = timezone.localtime().date()
    today_idx = today.weekday()
    wrong_idx = (today_idx + 3) % 7  # Ensure it's not today's weekday
    wrong_weekday = WEEKDAY_MAP[wrong_idx]

    daily_task = DailyTask.objects.create(
        user=user,
        title="Wrong Day",
        weekdays=[wrong_weekday],  # Today is excluded
        is_active=True,
    )

    generate_task_instances_for_week(daily_task.id)

    # May generate instances, but not for today
    today_instance = TaskInstance.objects.filter(date=today).first()
    assert today_instance is None


@pytest.mark.django_db
def test_list_task_instances(auth_client, user):
    task = DailyTask.objects.create(
        user=user, title="Listable", weekdays=["mon"], is_active=True
    )
    today = timezone.localdate()
    TaskInstance.objects.create(
        parent_daily_task=task, user=user, title="Listable", date=today
    )

    url = reverse("tasks_manager:task-instances-list")
    response = auth_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_toggle_task_instance(auth_client, user):
    task = DailyTask.objects.create(
        user=user, title="ToggleTest", weekdays=["mon"], is_active=True
    )
    today = timezone.localdate()
    instance = TaskInstance.objects.create(
        parent_daily_task=task,
        user=user,
        title="ToggleTest",
        date=today,
        is_completed=False,
    )

    url = reverse("tasks_manager:task-instances-toggle-complete", args=[instance.id])
    response = auth_client.post(url)

    assert response.status_code == 200
    assert response.data["is_completed"] is True

    # Toggle again
    response = auth_client.post(url)
    assert response.status_code == 200
    assert response.data["is_completed"] is False
