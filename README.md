# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Implementation Summary

The logic layer lives in [pawpal_system.py](pawpal_system.py) and is built from four classes:

- **Task** (dataclass): one care activity with a title, duration, `Priority` (LOW/MEDIUM/HIGH), preferred time of day, frequency, and completion status.
- **Pet** (dataclass): a pet's details plus its list of tasks. `add_task` tags each task with the pet's name so the plan can show who it is for.
- **Owner**: has a daily time budget and many pets. `get_all_tasks()` returns every pet's tasks in one list.
- **Scheduler**: the "brain". It reads from `owner.get_all_tasks()` (never from a single pet), keeps pending tasks, picks the highest-priority ones that fit the time budget, orders them by time of day, and records what was scheduled (`plan`) and skipped (`skipped`). `explain_plan()` turns that into readable reasoning.

Flow: `Owner` → `Pet`s → `Task`s are gathered by `Owner.get_all_tasks()`, then `Scheduler.build_daily_plan()` selects and orders them. Run `python main.py` for a terminal demo and `python -m pytest` for the tests.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py` (one owner, two pets, four tasks, 60 available minutes):

```
Today's Schedule for Sam
========================================================
Time       Task          Pet      Min  Priority
--------------------------------------------------------
morning    Morning walk  Max       30  HIGH
afternoon  Play session  Luna      15  MEDIUM
evening    Feed dinner   Luna      10  HIGH
--------------------------------------------------------
Skipped (not enough time):
  Grooming (Max), 40 min, LOW
--------------------------------------------------------
Total: 55 of 60 minutes

Planned 55 of 60 available minutes.
- Morning walk (Max): 30 min, HIGH priority, morning
- Play session (Luna): 15 min, MEDIUM priority, afternoon
- Feed dinner (Luna): 10 min, HIGH priority, evening
Skipped (not enough time left):
- Grooming (Max): 40 min, LOW priority
```

## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest
```

The 23 tests in `tests/test_pawpal.py` cover the core scheduling logic:

- **Task basics:** marking a task complete, adding a task to a pet, and validation (a duration of 0 or an unknown frequency raises `ValueError`).
- **Sorting:** `sort_by_time` returns tasks in chronological order, puts untimed tasks last, keeps the original order for ties, and works across multiple pets and with no tasks.
- **Recurrence:** completing a daily or weekly task adds the next copy (due 1 or 7 days later, counted from the task's due date). The copy is pending and keeps the original's time and pet. One-off tasks create nothing.
- **Conflict detection:** tasks at the same date and time are flagged, within one pet and across pets. Different days, untimed tasks and completed tasks are not flagged, and no tasks gives no warnings.
- **Plan building:** high-priority tasks are chosen first, tasks that don't fit are skipped, and a task that exactly fills the budget is allowed. Completed and not-yet-due tasks are excluded, and an owner with no tasks gets an empty plan.
- **Filtering:** by pet name and by completion status.

Sample output:

```
.......................                                                  [100%]
23 passed in 0.03s
```

## 📐 Smarter Scheduling

Beyond the priority-and-time-budget plan, the scheduler has four extra features. Run `python main.py` to see each one in the terminal.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | `Scheduler.sort_by_time()` | Orders tasks by their exact `time` ("HH:MM"). |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name, completion status, or both. |
| Conflict detection | `Scheduler.detect_conflicts()` | Warns when pending tasks share a date and start time. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a daily or weekly task creates the next one. |

**Sorting.** `sort_by_time()` uses `sorted()` with a lambda key, `(t.time == "", t.time)`. Zero-padded "HH:MM" strings already sort correctly as text, so no time parsing is needed. Tasks with no time go last.

**Filtering.** `filter_tasks(pet_name=None, completed=None)` returns the tasks that match every filter you pass. Leaving a filter as `None` means "any", so `filter_tasks(pet_name="Luna", completed=False)` gives Luna's pending tasks.

**Conflict detection.** `detect_conflicts()` groups pending tasks by `(due_date, time)` and returns a list of warning strings, one for each slot with more than one task. It never raises, and it checks across pets as well as within one pet. It only matches exact start times, not overlapping durations (for example, a 30-minute task at 09:00 and another at 09:15 are not flagged). That keeps it simple and predictable.

**Recurring tasks.** `Scheduler.mark_task_complete(task)` marks the task done. If its frequency is "daily" or "weekly", `Task.next_occurrence()` makes a copy due 1 day or 7 days later (using `timedelta`), and the scheduler adds it to the same pet. One-off ("once") tasks create nothing. `build_daily_plan()` ignores tasks that aren't due yet, so tomorrow's copy doesn't appear in today's plan.

## 📸 Demo Walkthrough
My confidence level would be 4. 

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
