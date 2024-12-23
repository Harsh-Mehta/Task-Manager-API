test_task_id: int = None


def test_create_task(client, task_payload):
    """Test to create a new task"""

    response = client.post("/tasks", json=task_payload)
    task = response.json()

    assert response.status_code == 200
    assert task["title"] == "New test task"
    assert task["description"] == "This is a test task"


def test_get_all_tasks(client):
    """Test to get all the tasks"""
    global test_task_id

    response = client.get("/tasks")

    tasks = response.json()["tasks"]
    test_task_id = tasks[0]["id"]

    assert response.status_code == 200
    assert isinstance(tasks, list)


def test_get_all_completed_tasks(client):
    """Test to get all the tasks that are completed"""

    response = client.get("/tasks", params={"completed": True})
    
    assert response.status_code == 200
    assert isinstance(response.json()["tasks"], list)


def test_get_task_by_id(client):
    """Test to get a task by its ID"""

    global test_task_id

    response = client.get(f"/tasks/{test_task_id}")
    task = response.json()["task"]

    assert response.status_code == 200
    assert task["title"] == "New test task"
    assert task["description"] == "This is a test task"
    assert task["completed"] is False


def test_get_task_by_invalid_id(client):
    """Test to get a task by an invalid ID"""

    response = client.get("/tasks/1000")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "No task not found with ID provided"


def test_partial_update_task(client):
    """Test to partially update the details of a task"""

    global test_task_id

    response = client.patch(f"/tasks/{test_task_id}", json={"title": "Updated Task"})
    
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"


def test_modify_task(client, task_payload_updated):
    """Test to modify the details of a task"""

    global test_task_id

    response = client.put(f"/tasks/{test_task_id}", json=task_payload_updated)
    task = response.json()
    
    assert response.status_code == 200
    assert task["title"] == "Modified task"
    assert task["description"] == "This is a modified task"


def test_delete_task(client):
    """Test to delete a task"""

    global test_task_id

    response = client.delete(f"/tasks/{test_task_id}")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Task has been deleted"

    response = client.get(f"/tasks/{test_task_id}")
    assert response.status_code == 404