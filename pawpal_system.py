"""PawPal+ logic layer: class skeletons based on diagrams/uml_draft.mmd."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    category: str
    duration_minutes: int
    priority: int
    preferred_time: str = ""
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        pass

    def get_pending_tasks(self) -> List[Task]:
        """Return tasks that are not yet completed."""
        pass


class Owner:
    def __init__(self, name: str, available_minutes_per_day: int) -> None:
        self.name = name
        self.available_minutes_per_day = available_minutes_per_day
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        pass

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Collect tasks across all of the owner's pets."""
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def build_daily_plan(self) -> List[Task]:
        """Select and order tasks that fit the owner's available time and priorities."""
        pass

    def explain_plan(self) -> str:
        """Explain why the plan was chosen."""
        pass
