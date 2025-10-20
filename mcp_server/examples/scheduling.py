"""
Scheduling Problem using Gurddy CSP Solver

Schedule tasks with constraints on time slots, resources, and dependencies.
"""

import gurddy

def solve_course_scheduling():
    """Solve a university course scheduling problem."""
    model = gurddy.Model("CourseScheduling", "CSP")

    # Courses to schedule
    courses = ['Math101', 'Physics101', 'Chemistry101', 'Biology101', 'English101']

    # Time slots (0=Mon9am, 1=Mon10am, 2=Mon11am, 3=Tue9am, etc.)
    # 5 days × 4 time slots = 20 total slots
    time_slots = list(range(20))

    # Variables: each course gets assigned to a time slot
    course_vars = {}
    for course in courses:
        course_vars[course] = model.addVar(course, domain=time_slots)

    # Constraint 1: No two courses at the same time
    model.addConstraint(gurddy.AllDifferentConstraint(list(course_vars.values())))

    # Constraint 2: Some courses cannot be on the same day
    # Math and Physics should not be on the same day (too intensive)
    def not_same_day(slot1, slot2):
        day1 = slot1 // 4  # 4 slots per day
        day2 = slot2 // 4
        return day1 != day2

    model.addConstraint(gurddy.FunctionConstraint(
        not_same_day,
        (course_vars['Math101'], course_vars['Physics101'])
    ))

    # Constraint 3: Chemistry should be in the morning (slots 0,1 of each day)
    def is_morning_slot(slot):
        return (slot % 4) < 2  # first 2 slots of each day

    # Convert to binary constraint by checking if Chemistry is in morning
    def chemistry_morning_constraint(chem_slot, _dummy_slot):
        return is_morning_slot(chem_slot)

    # Use a dummy variable for the constraint
    dummy_var = model.addVar("dummy", domain=[0])
    model.addConstraint(gurddy.FunctionConstraint(
        chemistry_morning_constraint,
        (course_vars['Chemistry101'], dummy_var)
    ))

    solution = model.solve()
    return solution, courses, time_slots

def solve_meeting_scheduling():
    """Solve a meeting room scheduling problem."""
    model = gurddy.Model("MeetingScheduling", "CSP")

    # Meetings to schedule
    meetings = ['TeamA', 'TeamB', 'TeamC', 'BoardMeeting', 'ClientCall']

    # Time slots: 8 slots per day (9am-5pm), 2 days
    time_slots = list(range(16))

    # Variables
    meeting_vars = {}
    for meeting in meetings:
        meeting_vars[meeting] = model.addVar(meeting, domain=time_slots)

    # Constraint 1: No overlapping meetings
    model.addConstraint(gurddy.AllDifferentConstraint(list(meeting_vars.values())))

    # Constraint 2: Board meeting must be in the afternoon (slots 4-7 each day)
    def is_afternoon(slot):
        return (slot % 8) >= 4

    def board_afternoon_constraint(board_slot, _dummy_slot):
        return is_afternoon(board_slot)

    dummy_var = model.addVar("dummy", domain=[0])
    model.addConstraint(gurddy.FunctionConstraint(
        board_afternoon_constraint,
        (meeting_vars['BoardMeeting'], dummy_var)
    ))

    # Constraint 3: TeamA and TeamB should not be on the same day
    def different_days(slot1, slot2):
        day1 = slot1 // 8
        day2 = slot2 // 8
        return day1 != day2

    model.addConstraint(gurddy.FunctionConstraint(
        different_days,
        (meeting_vars['TeamA'], meeting_vars['TeamB'])
    ))

    solution = model.solve()
    return solution, meetings, time_slots

def print_schedule(solution, items, time_slots, schedule_type="Schedule"):
    """Print the scheduling solution."""
    if not solution:
        print(f"No solution found for {schedule_type}!")
        return

    print(f"\n{schedule_type} Solution:")
    print("=" * 50)

    # Determine schedule parameters
    if len(time_slots) == 20:  # Course scheduling (5 days × 4 slots)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        slots_per_day = 4
        slot_names = ['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM']
    else:  # Meeting scheduling (2 days × 8 slots)
        days = ['Day 1', 'Day 2']
        slots_per_day = 8
        slot_names = ['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM',
                     '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM']

    # Create reverse mapping: slot -> item
    slot_to_item = {}
    for item in items:
        if item in solution:  # Skip dummy variables
            slot = solution[item]
            slot_to_item[slot] = item

    # Print schedule
    for day_idx, day in enumerate(days):
        print(f"\n{day}:")
        print("-" * 20)
        for slot_idx in range(slots_per_day):
            absolute_slot = day_idx * slots_per_day + slot_idx
            time = slot_names[slot_idx]
            item = slot_to_item.get(absolute_slot, "Free")
            print(f"{time:>10}: {item}")

    # Print summary
    print("\nScheduled items:")
    for item in sorted(items):
        if item in solution:
            slot = solution[item]
            day_idx = slot // slots_per_day
            slot_idx = slot % slots_per_day
            day_name = days[day_idx]
            time_name = slot_names[slot_idx]
            print(f"{item:>15}: {day_name} {time_name}")

def solve_resource_scheduling():
    """Solve a resource allocation scheduling problem."""
    model = gurddy.Model("ResourceScheduling", "CSP")

    # Tasks that need resources
    tasks = ['TaskA', 'TaskB', 'TaskC', 'TaskD']

    # Resources available (0=Resource1, 1=Resource2, 2=Resource3)
    resources = list(range(3))

    # Time slots (0-7 for 8 time periods)
    time_slots = list(range(8))

    # Variables: each task gets assigned a resource and time slot
    # We'll encode this as: value = resource * 8 + time_slot
    # So domain is [0-23] representing all resource-time combinations
    task_vars = {}
    domain = []
    for resource in resources:
        for time_slot in time_slots:
            domain.append(resource * 8 + time_slot)

    for task in tasks:
        task_vars[task] = model.addVar(task, domain=domain)

    # Constraint 1: No two tasks can use the same resource at the same time
    model.addConstraint(gurddy.AllDifferentConstraint(list(task_vars.values())))

    # Constraint 2: TaskA must use Resource1 (resource 0)
    def task_a_resource1(assignment, _dummy):
        resource = assignment // 8
        return resource == 0

    dummy_var = model.addVar("dummy", domain=[0])
    model.addConstraint(gurddy.FunctionConstraint(
        task_a_resource1,
        (task_vars['TaskA'], dummy_var)
    ))

    solution = model.solve()
    return solution, tasks, resources, time_slots

def print_resource_schedule(solution, tasks, resources, time_slots):
    """Print the resource scheduling solution."""
    if not solution:
        print("No solution found for Resource Scheduling!")
        return

    print("\nResource Scheduling Solution:")
    print("=" * 50)

    # Decode assignments
    assignments = {}
    for task in tasks:
        if task in solution:
            encoded = solution[task]
            resource = encoded // 8
            time_slot = encoded % 8
            assignments[task] = (resource, time_slot)

    # Print by task
    print("Task Assignments:")
    for task in sorted(tasks):
        if task in assignments:
            resource, time_slot = assignments[task]
            print(f"{task:>8}: Resource{resource+1} at Time{time_slot+1}")

    # Print resource utilization
    print("\nResource Utilization:")
    for resource in resources:
        print(f"\nResource{resource+1}:")
        for time_slot in time_slots:
            assigned_task = None
            for task, (r, t) in assignments.items():
                if r == resource and t == time_slot:
                    assigned_task = task
                    break
            status = assigned_task if assigned_task else "Free"
            print(f"  Time{time_slot+1}: {status}")

if __name__ == "__main__":
    # Solve course scheduling
    print("Solving Course Scheduling Problem...")
    course_solution, course_list, course_slots = solve_course_scheduling()
    print_schedule(course_solution, course_list, course_slots, "Course Schedule")

    # Solve meeting scheduling
    print("\n" + "="*60)
    print("Solving Meeting Scheduling Problem...")
    meeting_solution, meeting_list, meeting_slots = solve_meeting_scheduling()
    print_schedule(meeting_solution, meeting_list, meeting_slots, "Meeting Schedule")

    # Solve resource scheduling
    print("\n" + "="*60)
    print("Solving Resource Scheduling Problem...")
    resource_solution, task_list, resource_list, resource_slots = solve_resource_scheduling()
    print_resource_schedule(resource_solution, task_list, resource_list, resource_slots)