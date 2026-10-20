from pawpal_system import Pet, Priority, Task


def make_task() -> Task:
    return Task("Morning walk", "exercise", 30, Priority.HIGH)


def test_mark_complete_changes_status():
    task = make_task()
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet("Max", "dog", 3)
    assert len(pet.tasks) == 0

    pet.add_task(make_task())

    assert len(pet.tasks) == 1
