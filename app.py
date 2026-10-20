import streamlit as st

from pawpal_system import Owner, Pet, Priority, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Plan pet care tasks around your time and priorities.")

# Streamlit reruns this script on every click, so keep the Owner in session_state.
# It is only created the first time; later reruns reuse the same object.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", available_minutes_per_day=60)
owner: Owner = st.session_state.owner

st.divider()

# --- Owner ---
st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    owner.name = st.text_input("Owner name", value=owner.name)
with col2:
    owner.available_minutes_per_day = int(
        st.number_input(
            "Minutes available per day",
            min_value=1,
            max_value=1440,
            value=owner.available_minutes_per_day,
        )
    )

# --- Pets ---
st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        new_pet_name = st.text_input("Pet name")
    with c2:
        new_species = st.selectbox("Species", ["dog", "cat", "other"])
    with c3:
        new_age = st.number_input("Age", min_value=0, max_value=40, value=1)
    if st.form_submit_button("Add pet"):
        if not new_pet_name.strip():
            st.error("Please enter a pet name.")
        elif any(p.name == new_pet_name.strip() for p in owner.pets):
            st.error(f"You already have a pet named {new_pet_name.strip()}.")
        else:
            owner.add_pet(Pet(new_pet_name.strip(), new_species, int(new_age)))
            st.success(f"Added {new_pet_name.strip()}!")

if owner.pets:
    st.table(
        [{"Name": p.name, "Species": p.species, "Age": p.age, "Tasks": len(p.tasks)} for p in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

# --- Tasks ---
st.subheader("Tasks")
if not owner.pets:
    st.caption("Add a pet first, then you can give it tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        target_name = st.selectbox("For which pet?", [p.name for p in owner.pets])
        c1, c2 = st.columns(2)
        with c1:
            title = st.text_input("Task title", placeholder="Morning walk")
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
            priority_name = st.selectbox("Priority", [p.name for p in Priority], index=2)
        with c2:
            category = st.text_input("Category", placeholder="exercise")
            preferred_time = st.selectbox("Preferred time", ["morning", "afternoon", "evening"])
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        if st.form_submit_button("Add task"):
            if not title.strip():
                st.error("Please enter a task title.")
            else:
                pet = next(p for p in owner.pets if p.name == target_name)
                pet.add_task(
                    Task(
                        title.strip(),
                        category.strip() or "general",
                        int(duration),
                        Priority[priority_name],
                        preferred_time=preferred_time,
                        frequency=frequency,
                    )
                )
                st.success(f"Added '{title.strip()}' to {target_name}.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.table(
        [
            {
                "Pet": t.pet_name,
                "Task": t.title,
                "Minutes": t.duration_minutes,
                "Priority": t.priority.name,
                "Time": t.preferred_time,
                "Frequency": t.frequency,
            }
            for t in all_tasks
        ]
    )
elif owner.pets:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule ---
st.subheader("Today's Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.build_daily_plan()
    if not plan and not scheduler.skipped:
        st.warning("There are no pending tasks to schedule.")
    else:
        used = sum(t.duration_minutes for t in plan)
        st.success(f"Planned {used} of {owner.available_minutes_per_day} available minutes.")
        if plan:
            st.table(
                [
                    {
                        "Time": t.preferred_time or "anytime",
                        "Task": t.title,
                        "Pet": t.pet_name,
                        "Minutes": t.duration_minutes,
                        "Priority": t.priority.name,
                    }
                    for t in plan
                ]
            )
        if scheduler.skipped:
            st.warning(
                "Skipped (not enough time): "
                + ", ".join(f"{t.title} ({t.pet_name}, {t.duration_minutes} min)" for t in scheduler.skipped)
            )
        with st.expander("Why this plan?"):
            st.text(scheduler.explain_plan())
