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

    scheduler = Scheduler(owner)
    scheduler.build_daily_plan()
    print_schedule(scheduler)
    print()
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
