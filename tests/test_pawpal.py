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


# ---- Edge cases ----

import pytest


def test_sort_by_time_with_no_tasks_returns_empty():
    sched, _ = make_scheduler()
    assert sched.sort_by_time() == []


def test_sort_by_time_keeps_original_order_for_equal_times():
    sched, pet = make_scheduler()
    pet.add_task(Task("first", "x", 5, Priority.LOW, time="09:00"))
    pet.add_task(Task("second", "x", 5, Priority.LOW, time="09:00"))
    assert [t.title for t in sched.sort_by_time()] == ["first", "second"]


def test_sort_by_time_works_across_multiple_pets():
    sched, pet = make_scheduler()
    other = Pet("Luna", "cat", 2)
    sched.owner.add_pet(other)
    pet.add_task(Task("late", "x", 5, Priority.LOW, time="18:00"))
    other.add_task(Task("early", "x", 5, Priority.LOW, time="07:00"))
    assert [t.title for t in sched.sort_by_time()] == ["early", "late"]


def test_daily_recurrence_copy_is_pending_and_original_stays_complete():
    sched, pet = make_scheduler()
    task = Task("feed", "x", 5, Priority.HIGH, frequency="daily", time="08:00")
    pet.add_task(task)
    nxt = sched.mark_task_complete(task)
    assert task.completed is True
    assert nxt is not task and nxt.completed is False
    assert nxt.time == "08:00" and nxt.pet_name == "Max"


def test_recurrence_is_based_on_due_date_not_today():
    sched, pet = make_scheduler()
    due = date(2025, 1, 31)
    task = Task("feed", "x", 5, Priority.HIGH, frequency="daily", due_date=due)
    pet.add_task(task)
    assert sched.mark_task_complete(task).due_date == date(2025, 2, 1)


def test_recurring_task_not_attached_to_a_pet_does_not_crash():
    sched, _ = make_scheduler()
    orphan = Task("feed", "x", 5, Priority.HIGH, frequency="daily")
    assert sched.mark_task_complete(orphan).due_date == date.today() + timedelta(days=1)


def test_conflict_detected_across_different_pets():
    sched, pet = make_scheduler()
    other = Pet("Luna", "cat", 2)
    sched.owner.add_pet(other)
    pet.add_task(Task("walk", "x", 5, Priority.LOW, time="09:00"))
    other.add_task(Task("feed", "x", 5, Priority.LOW, time="09:00"))
    warnings = sched.detect_conflicts()
    assert len(warnings) == 1
    assert "Max" in warnings[0] and "Luna" in warnings[0]


def test_no_conflicts_when_no_tasks_or_all_times_unique():
    sched, pet = make_scheduler()
    assert sched.detect_conflicts() == []
    pet.add_task(Task("a", "x", 5, Priority.LOW, time="09:00"))
    pet.add_task(Task("b", "x", 5, Priority.LOW, time="09:01"))
    assert sched.detect_conflicts() == []


def test_same_time_on_different_days_or_untimed_is_not_a_conflict():
    sched, pet = make_scheduler()
    pet.add_task(Task("a", "x", 5, Priority.LOW, time="09:00"))
    pet.add_task(Task("b", "x", 5, Priority.LOW, time="09:00",
                      due_date=date.today() + timedelta(days=1)))
    pet.add_task(Task("c", "x", 5, Priority.LOW))
    pet.add_task(Task("d", "x", 5, Priority.LOW))
    assert sched.detect_conflicts() == []


def test_completed_tasks_do_not_cause_conflicts():
    sched, pet = make_scheduler()
    done = Task("a", "x", 5, Priority.LOW, time="09:00")
    pet.add_task(done)
    pet.add_task(Task("b", "x", 5, Priority.LOW, time="09:00"))
    done.mark_complete()
    assert sched.detect_conflicts() == []


def test_pet_with_no_tasks_gives_empty_plan_and_explanation():
    sched, _ = make_scheduler()
    assert sched.build_daily_plan() == []
    assert "No plan yet" in sched.explain_plan()


def test_plan_prefers_high_priority_and_skips_what_does_not_fit():
    owner = Owner("Sam", 30)
    pet = Pet("Max", "dog", 3)
    owner.add_pet(pet)
    pet.add_task(Task("low", "x", 10, Priority.LOW))
    pet.add_task(Task("big", "x", 40, Priority.HIGH))
    pet.add_task(Task("high", "x", 30, Priority.MEDIUM))
    sched = Scheduler(owner)
    plan = sched.build_daily_plan()
    assert [t.title for t in plan] == ["high"]
    assert {t.title for t in sched.skipped} == {"big", "low"}


def test_plan_allows_task_that_exactly_fills_budget():
    owner = Owner("Sam", 30)
    pet = Pet("Max", "dog", 3)
    owner.add_pet(pet)
    pet.add_task(Task("exact", "x", 30, Priority.LOW))
    assert len(Scheduler(owner).build_daily_plan()) == 1


def test_plan_excludes_completed_tasks_and_orders_by_time_of_day():
    sched, pet = make_scheduler()
    done = Task("done", "x", 5, Priority.HIGH)
    pet.add_task(done)
    done.mark_complete()
    pet.add_task(Task("eve", "x", 5, Priority.HIGH, preferred_time="evening"))
    pet.add_task(Task("morn", "x", 5, Priority.LOW, preferred_time="morning"))
    assert [t.title for t in sched.build_daily_plan()] == ["morn", "eve"]


def test_task_validation_rejects_bad_duration_and_frequency():
    with pytest.raises(ValueError):
        Task("x", "x", 0, Priority.LOW)
    with pytest.raises(ValueError):
        Task("x", "x", 5, Priority.LOW, frequency="monthly")
