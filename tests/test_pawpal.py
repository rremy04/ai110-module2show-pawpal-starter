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


from datetime import date, timedelta

from pawpal_system import Owner, Scheduler


def make_scheduler():
    owner = Owner("Sam", 120)
    pet = Pet("Max", "dog", 3)
    owner.add_pet(pet)
    return Scheduler(owner), pet


def test_sort_by_time_orders_hhmm_and_puts_untimed_last():
    sched, pet = make_scheduler()
    pet.add_task(Task("c", "x", 5, Priority.LOW))
    pet.add_task(Task("b", "x", 5, Priority.LOW, time="14:00"))
    pet.add_task(Task("a", "x", 5, Priority.LOW, time="08:30"))
    assert [t.title for t in sched.sort_by_time()] == ["a", "b", "c"]


def test_filter_by_pet_and_status():
    sched, pet = make_scheduler()
    done = Task("done", "x", 5, Priority.LOW)
    pet.add_task(done)
    pet.add_task(Task("todo", "x", 5, Priority.LOW))
    done.mark_complete()
    assert [t.title for t in sched.filter_tasks(completed=True)] == ["done"]
    assert [t.title for t in sched.filter_tasks(pet_name="Max", completed=False)] == ["todo"]
    assert sched.filter_tasks(pet_name="Nobody") == []


def test_daily_and_weekly_tasks_create_next_occurrence():
    sched, pet = make_scheduler()
    daily = Task("feed", "x", 5, Priority.HIGH, frequency="daily")
    weekly = Task("brush", "x", 5, Priority.LOW, frequency="weekly")
    pet.add_task(daily)
    pet.add_task(weekly)
    assert sched.mark_task_complete(daily).due_date == date.today() + timedelta(days=1)
    assert sched.mark_task_complete(weekly).due_date == date.today() + timedelta(weeks=1)
    assert len(pet.tasks) == 4


def test_one_off_task_creates_no_next_occurrence():
    sched, pet = make_scheduler()
    task = Task("vet", "x", 5, Priority.HIGH)
    pet.add_task(task)
    assert sched.mark_task_complete(task) is None
    assert len(pet.tasks) == 1


def test_conflict_detection_warns_instead_of_crashing():
    sched, pet = make_scheduler()
    pet.add_task(Task("a", "x", 5, Priority.LOW, time="09:00"))
    pet.add_task(Task("b", "x", 5, Priority.LOW, time="09:00"))
    pet.add_task(Task("c", "x", 5, Priority.LOW, time="10:00"))
    warnings = sched.detect_conflicts()
    assert len(warnings) == 1 and "09:00" in warnings[0]


def test_plan_skips_tasks_not_due_yet():
    sched, pet = make_scheduler()
    pet.add_task(Task("later", "x", 5, Priority.HIGH, due_date=date.today() + timedelta(days=1)))
    assert sched.build_daily_plan() == []
