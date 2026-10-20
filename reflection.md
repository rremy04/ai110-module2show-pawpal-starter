# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
- They want to be able to Track pet care tasks for example walks, feeding. Consider constraints for example time available, priority and produce a daily plan and explain why it chose that plan
- I think we would need, Owner, Pet, Task, Scheduler
- My initial UML has four classes. Owner holds the owner's name and daily available time, and manages their pets. Pet holds basic info like name and species, and keeps the list of care tasks for that pet. Task represents a single care activity, such as a walk or feeding, with a duration, priority, preferred time, and completion status. Scheduler takes an Owner, picks and orders tasks that fit the available time and priorities, and explains why it chose that plan. The relationships are simple: an Owner has Pets, a Pet has Tasks, and the Scheduler plans for one Owner.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
- priority went from being an into to a Priority enum because when it was an int it couldn't differentiate whether 1 or 5 were the most important therefore this could affect the logic but wouldn't necessarily appear as an error. Enum allows us to make the values meaning more obvious and ensures a validity check so that invalid values can't be created.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
- The scheduler considers three things: the owner's available minutes per day, each task's priority (LOW, MEDIUM, HIGH), and each task's preferred time of day (morning, afternoon, evening). It also ignores tasks that are already completed.
- I ranked them in that order of importance. Time is a hard limit, because the owner can't do more than they have time for. Priority decides which tasks get a place in the plan, so important care like feeding isn't dropped for something optional. Preferred time is only a soft preference, so it just decides the order of the tasks that were chosen.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
- The scheduler is greedy: it takes tasks from highest to lowest priority and skips any task that doesn't fit in the time left, then keeps going with smaller ones. This isn't always the best use of time. For example, with 60 minutes it might schedule a 30-minute HIGH task and a 15-minute MEDIUM task and leave 15 minutes unused, even though a different combination could have used all 60.
- This is reasonable because the plan is easy to understand and explain, which is one of the app's goals, and it always puts the most important care first. For a busy pet owner with a handful of daily tasks, a simple predictable plan matters more than squeezing out every last minute.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
- I used AI to turn my four brainstormed classes into a Mermaid UML diagram, generate dataclass skeletons from it, review the skeleton for missing relationships and bottlenecks, and then flesh out the full logic. The most helpful prompts were specific ones: asking it to review my skeleton for missing relationships, and asking how the Scheduler should retrieve tasks from the Owner's pets.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
- **What AI suggested:** the skeleton review listed about ten issues, including a missing link between Task and Pet, no place to store the Scheduler's plan, an ambiguous integer priority, recurring tasks, validation, and making Owner a dataclass.
- **What I accepted:** the three I judged most important, which were `pet_name` on Task, `plan` and `skipped` on Scheduler, and the Priority enum. The AI also suggested other options for where tasks should live, but I questioned why a Pet would have a task and kept tasks on Pet because tasks usually belong to one animal.
- **What I did not accept yet:** I held off on recurring-task logic and making Owner a dataclass. `frequency` is stored but not used by the scheduler yet, so a daily task stays completed until it is reset.
- **How I verified:** I ran `python main.py` and checked that the schedule respected the 60-minute limit, skipped the low-priority grooming task, and included tasks from both pets. I also wrote two pytest tests, one for `mark_complete()` and one for `add_task()`, and ran `python -m pytest` to confirm they pass.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
