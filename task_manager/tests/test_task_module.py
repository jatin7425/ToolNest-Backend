# task_manager/tests/test_task_module.py
import pytest
from django.urls import reverse
from task_manager.models.models import Task


@pytest.mark.django_db
def test_task_creation(auth_client):
    url = reverse("tasks_manager:tasks-list")
    data = {
        "title": "Write tests",
        "description": "Write test cases for Task module",
        "priority": "high",
    }
    response = auth_client.post(url, data)
    assert response.status_code == 201
    assert response.data["title"] == "Write tests"


@pytest.mark.django_db
def test_task_list(auth_client, user):
    Task.objects.create(user=user, title="Task 1")
    Task.objects.create(user=user, title="Task 2")
    url = reverse("tasks_manager:tasks-list")
    response = auth_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_task_filter_by_title(auth_client, user):
    Task.objects.create(user=user, title="Match me")
    Task.objects.create(user=user, title="Skip me")
    url = reverse("tasks_manager:tasks-list") + "?title=Match"
    response = auth_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "Match me"


@pytest.mark.django_db
def test_task_update(auth_client, user):
    task = Task.objects.create(user=user, title="Old Title")
    url = reverse("tasks_manager:tasks-detail", args=[task.id])
    response = auth_client.patch(url, {"title": "New Title"})
    assert response.status_code == 200
    assert response.data["title"] == "New Title"


@pytest.mark.django_db
def test_task_delete(auth_client, user):
    task = Task.objects.create(user=user, title="Delete me")
    url = reverse("tasks_manager:tasks-detail", args=[task.id])
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert Task.objects.count() == 0


@pytest.mark.django_db
def test_toggle_is_completed(auth_client, user):
    task = Task.objects.create(user=user, title="Toggle task")
    url = reverse("tasks_manager:tasks-toggle-complete", args=[task.id])

    # Toggle on
    response = auth_client.post(url)
    assert response.status_code == 200
    assert response.data["is_completed"] is True

    # Toggle off
    response = auth_client.post(url)
    assert response.status_code == 200
    assert response.data["is_completed"] is False
