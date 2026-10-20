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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
