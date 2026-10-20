"""Temporary testing ground: run the PawPal+ logic in the terminal."""

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def print_schedule(scheduler: Scheduler) -> None:
    owner = scheduler.owner
    print(f"Today's Schedule for {owner.name}")
    print("=" * 56)
    print(f"{'Time':<11}{'Task':<14}{'Pet':<8}{'Min':>4}  Priority")
    print("-" * 56)
    for t in scheduler.plan:
        print(
            f"{t.preferred_time or 'anytime':<11}{t.title:<14}{t.pet_name:<8}"
            f"{t.duration_minutes:>4}  {t.priority.name}"
        )
    print("-" * 56)
    if scheduler.skipped:
        print("Skipped (not enough time):")
        for t in scheduler.skipped:
            print(f"  {t.title} ({t.pet_name}), {t.duration_minutes} min, {t.priority.name}")
        print("-" * 56)
    used = sum(t.duration_minutes for t in scheduler.plan)
    print(f"Total: {used} of {owner.available_minutes_per_day} minutes")


def main() -> None:
    owner = Owner("Sam", available_minutes_per_day=60)

    max_dog = Pet("Max", "dog", 3)
    luna = Pet("Luna", "cat", 5)
    owner.add_pet(max_dog)
    owner.add_pet(luna)

    max_dog.add_task(Task("Morning walk", "exercise", 30, Priority.HIGH, preferred_time="morning"))
    max_dog.add_task(Task("Grooming", "care", 40, Priority.LOW))
    luna.add_task(Task("Feed dinner", "feeding", 10, Priority.HIGH, preferred_time="evening", frequency="daily"))
    luna.add_task(Task("Play session", "play", 15, Priority.MEDIUM, preferred_time="afternoon"))

    # Added out of order on purpose, with exact times, to exercise the new features.
    luna.add_task(Task("Evening meds", "health", 5, Priority.HIGH, time="18:30"))
    max_dog.add_task(Task("Vet call", "health", 10, Priority.MEDIUM, time="09:00"))
    luna.add_task(Task("Brush fur", "care", 10, Priority.LOW, time="07:15", frequency="weekly"))
    max_dog.add_task(Task("Training", "exercise", 20, Priority.MEDIUM, time="09:00"))  # clashes with Vet call

    scheduler = Scheduler(owner)

    print("Sorted by time:")
    for t in scheduler.sort_by_time():
        print(f"  {t.time or '--:--'}  {t.title} ({t.pet_name})")

    print("\nConflict check:")
    for warning in scheduler.detect_conflicts() or ["No conflicts."]:
        print(f"  {warning}")

    print("\nRecurring: completing 'Feed dinner' (daily) and 'Brush fur' (weekly)")
    for t in list(luna.tasks):
        if t.title in ("Feed dinner", "Brush fur"):
            new = scheduler.mark_task_complete(t)
            print(f"  {t.title}: next due {new.due_date}")
    scheduler.mark_task_complete(max_dog.tasks[0])  # "once" task: no new copy
    print(f"  Luna tasks: {len(luna.tasks)}, Max tasks: {len(max_dog.tasks)}")

    print("\nFilter: Luna's pending tasks")
    for t in scheduler.filter_tasks(pet_name="Luna", completed=False):
        print(f"  {t.title} due {t.due_date}")
    print("Filter: all completed tasks")
    for t in scheduler.filter_tasks(completed=True):
        print(f"  {t.title} ({t.pet_name})")

    print()
    scheduler.build_daily_plan()
    print_schedule(scheduler)
    print()
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
