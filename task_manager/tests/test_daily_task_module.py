import pytest
from rest_framework.reverse import reverse
from rest_framework import status
from task_manager.models.models import DailyTask


@pytest.mark.django_db
def test_create_daily_task(auth_client, user):
    payload = {
        "title": "Morning Routine",
        "description": "Stretching and Journaling",
        "priority": "high",
        "weekdays": ["mon", "tue", "wed"],
        "is_active": True,
    }

    url = reverse("tasks_manager:daily-tasks-list")
    response = auth_client.post(url, data=payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == payload["title"]
    assert set(response.data["weekdays"]) == set(payload["weekdays"])
    assert response.data["is_active"] is True


@pytest.mark.django_db
def test_list_daily_tasks(auth_client, user):
    DailyTask.objects.create(
        user=user, title="Task A", weekdays=["mon", "wed"], is_active=True
    )
    DailyTask.objects.create(
        user=user, title="Task B", weekdays=["fri"], is_active=False
    )

    url = reverse("tasks_manager:daily-tasks-list")
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data["results"], list)
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_read_daily_task(auth_client, user):
    task = DailyTask.objects.create(
        user=user, title="ReadMe", weekdays=["thu"], is_active=True
    )

    url = reverse("tasks_manager:daily-tasks-detail", args=[task.id])
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "ReadMe"


@pytest.mark.django_db
def test_update_daily_task(auth_client, user):
    task = DailyTask.objects.create(user=user, title="Old", weekdays=["mon"])

    updated = {
        "title": "Updated",
        "description": "Updated description",
        "priority": "high",
        "weekdays": ["tue", "wed"],
        "is_active": False,
    }

    url = reverse("tasks_manager:daily-tasks-detail", args=[task.id])
    response = auth_client.put(url, data=updated, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Updated"
    assert response.data["is_active"] is False


@pytest.mark.django_db
def test_partial_update_daily_task(auth_client, user):
    task = DailyTask.objects.create(user=user, title="Partial", weekdays=["fri"])

    url = reverse("tasks_manager:daily-tasks-detail", args=[task.id])
    response = auth_client.patch(
        url, data={"title": "Partially Updated"}, format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Partially Updated"


@pytest.mark.django_db
def test_delete_daily_task(auth_client, user):
    task = DailyTask.objects.create(user=user, title="DeleteMe", weekdays=["sun"])

    url = reverse("tasks_manager:daily-tasks-detail", args=[task.id])
    response = auth_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert DailyTask.objects.filter(id=task.id).count() == 0


@pytest.mark.django_db
def test_toggle_daily_task_complete(auth_client, user):
    task = DailyTask.objects.create(
        user=user, title="Daily Test", weekdays=["mon"], is_active=True
    )

    url = reverse("tasks_manager:daily-tasks-toggle-complete", args=[task.id])

    # Toggle once → should become False
    response = auth_client.post(url)
    assert response.status_code == 200
    assert response.data["is_active"] is False

    # Toggle again → should become True
    response = auth_client.post(url)
    assert response.status_code == 200
    assert response.data["is_active"] is True
