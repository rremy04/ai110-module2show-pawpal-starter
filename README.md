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

## ✨ Features

- **Priority-based daily plan:** tasks are considered highest priority first (shorter tasks win ties) and added until the owner's daily minutes run out. A task that doesn't fit is skipped, but smaller ones can still fill the remaining time.
- **Time-of-day ordering:** the chosen tasks are ordered morning, afternoon, evening. Tasks with no preferred time go last.
- **Sorting by start time:** `sort_by_time()` lists tasks by their exact "HH:MM" time, earliest first, with untimed tasks at the end.
- **Filtering:** `filter_tasks()` narrows the list by pet, by completed or pending, or both.
- **Conflict warnings:** `detect_conflicts()` warns when two or more pending tasks share the same date and start time, across pets or within one. It returns warnings and never crashes.
- **Daily and weekly recurrence:** completing a recurring task automatically adds the next one to the same pet, due 1 or 7 days later. One-off tasks don't repeat.
- **Due dates:** tasks that aren't due yet (such as tomorrow's copy of a daily task) stay out of today's plan.
- **Plan explanations:** `explain_plan()` says what was scheduled, what was skipped, and why.
- **Input validation:** a duration of 0 or an unknown frequency is rejected with a clear error.

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

Run the app with `streamlit run app.py`. The page is one scrolling screen, top to bottom.

### What you can do in the UI

- **Owner:** set your name and how many minutes you have each day.
- **Pets:** add a pet with a name, species and age. The pet table shows how many tasks each pet has. Empty or duplicate names are rejected.
- **Tasks:** add a task for a pet with a title, category, duration, priority, preferred time of day and frequency (once, daily or weekly). You can also give it an exact start time.
- **Task list:** filter by pet and by status (all, pending, completed). The table is sorted by start time, with a ✅ on finished tasks.
- **Mark complete:** pick a pending task and mark it done. If it repeats, the next copy appears automatically.
- **Today's Schedule:** press "Generate schedule" to get the plan, any skipped tasks, and a "Why this plan?" explanation.

### Example workflow

1. Set your name and daily minutes (for example, 60).
2. Add a pet, such as Max the dog, then another, such as Luna the cat.
3. Add tasks. Give "Vet call" and "Training" the same exact start time, 09:00.
4. A yellow warning appears above the task list naming both tasks and suggesting you move one to a different time.
5. Change the filters to see only Luna's pending tasks. The list stays sorted by start time.

### Scheduler behaviors you will see

- **Sorting:** the task list is always ordered by start time, with untimed tasks last.
- **Conflict warnings:** two pending tasks at the same date and time are flagged. Overlapping durations are not.
- **Recurrence:** completing a daily or weekly task creates its next occurrence, which stays out of today's plan until it is due.
- **Fitting the time budget:** high-priority tasks are scheduled first, and what doesn't fit is listed as skipped.

### Sample CLI output

Output from `python main.py`, which runs the same Scheduler logic in the terminal (dates depend on the day you run it):

```
Sorted by time:
  07:15  Brush fur (Luna)
  09:00  Vet call (Max)
  09:00  Training (Max)
  18:30  Evening meds (Luna)
  --:--  Morning walk (Max)
  --:--  Grooming (Max)
  --:--  Feed dinner (Luna)
  --:--  Play session (Luna)

Conflict check:
  Warning: 2 tasks at 09:00 on 2026-10-19: Vet call (Max), Training (Max)

Recurring: completing 'Feed dinner' (daily) and 'Brush fur' (weekly)
  Feed dinner: next due 2026-10-20
  Brush fur: next due 2026-10-26
  Luna tasks: 6, Max tasks: 4

Filter: Luna's pending tasks
  Play session due 2026-10-19
  Evening meds due 2026-10-19
  Feed dinner due 2026-10-20
  Brush fur due 2026-10-26
Filter: all completed tasks
  Morning walk (Max)
  Feed dinner (Luna)
  Brush fur (Luna)

Today's Schedule for Sam
========================================================
Time       Task          Pet      Min  Priority
--------------------------------------------------------
afternoon  Play session  Luna      15  MEDIUM
anytime    Evening meds  Luna       5  HIGH
anytime    Vet call      Max       10  MEDIUM
anytime    Training      Max       20  MEDIUM
--------------------------------------------------------
Skipped (not enough time):
  Grooming (Max), 40 min, LOW
--------------------------------------------------------
Total: 50 of 60 minutes

Planned 50 of 60 available minutes.
- Play session (Luna): 15 min, MEDIUM priority, afternoon
- Evening meds (Luna): 5 min, HIGH priority
- Vet call (Max): 10 min, MEDIUM priority
- Training (Max): 20 min, MEDIUM priority
Skipped (not enough time left):
- Grooming (Max): 40 min, LOW priority
```
