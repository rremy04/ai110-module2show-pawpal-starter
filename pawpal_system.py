"""PawPal+ logic layer: Task, Pet, Owner and Scheduler (see diagrams/uml_draft.mmd)."""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import List

# Sort order for time-of-day preferences; unknown or empty values go last.
TIME_ORDER = {"morning": 0, "afternoon": 1, "evening": 2}
FREQUENCIES = ("once", "daily", "weekly")


class Priority(IntEnum):
    """Higher value means more important."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    """A single pet care activity."""

    title: str
    category: str
    duration_minutes: int
    priority: Priority
    pet_name: str = ""
    preferred_time: str = ""
    frequency: str = "once"
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate duration and frequency when a task is created."""
        if self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be positive")
        if self.frequency not in FREQUENCIES:
            raise ValueError(f"frequency must be one of {FREQUENCIES}")

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def reset(self) -> None:
        """Mark this task as not done, e.g. at the start of a new day."""
        self.completed = False


@dataclass
class Pet:
    """A pet and the care tasks assigned to it."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet (matched by identity, not equality)."""
        self.tasks = [t for t in self.tasks if t is not task]

    def get_pending_tasks(self) -> List[Task]:
        """Return tasks that are not yet completed."""
        return [t for t in self.tasks if not t.completed]


class Owner:
    """A pet owner with a daily time budget and one or more pets."""

    def __init__(self, name: str, available_minutes_per_day: int) -> None:
        """Create an owner with a daily time budget and no pets yet."""
        self.name = name
        self.available_minutes_per_day = available_minutes_per_day
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner (matched by identity)."""
        self.pets = [p for p in self.pets if p is not pet]

    def get_all_tasks(self) -> List[Task]:
        """Collect every task across all of the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Builds and explains a daily plan from all of an owner's pets' tasks."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for one owner with an empty plan."""
        self.owner = owner
        self.plan: List[Task] = []
        self.skipped: List[Task] = []

    def build_daily_plan(self) -> List[Task]:
        """Pick pending tasks by priority until the owner's time runs out.

        Tasks are considered highest priority first (shorter tasks win ties).
        A task that doesn't fit is skipped, and smaller ones may still fill the
        remaining time. The chosen tasks are then ordered by preferred time of day.
        """
        pending = [t for t in self.owner.get_all_tasks() if not t.completed]
        by_importance = sorted(pending, key=lambda t: (-t.priority, t.duration_minutes))

        remaining = self.owner.available_minutes_per_day
        self.plan = []
        self.skipped = []
        for task in by_importance:
            if task.duration_minutes <= remaining:
                self.plan.append(task)
                remaining -= task.duration_minutes
            else:
                self.skipped.append(task)

        self.plan.sort(key=lambda t: TIME_ORDER.get(t.preferred_time, len(TIME_ORDER)))
        return self.plan

    def explain_plan(self) -> str:
        """Explain why each task was scheduled or skipped."""
        if not self.plan and not self.skipped:
            return "No plan yet, or no pending tasks to schedule."

        budget = self.owner.available_minutes_per_day
        used = sum(t.duration_minutes for t in self.plan)
        lines = [f"Planned {used} of {budget} available minutes."]
        for t in self.plan:
            when = f", {t.preferred_time}" if t.preferred_time else ""
            lines.append(
                f"- {t.title} ({t.pet_name}): {t.duration_minutes} min, "
                f"{t.priority.name} priority{when}"
            )
        if self.skipped:
            lines.append("Skipped (not enough time left):")
            for t in self.skipped:
                lines.append(
                    f"- {t.title} ({t.pet_name}): {t.duration_minutes} min, "
                    f"{t.priority.name} priority"
                )
        return "\n".join(lines)
