
def list_scheduling(jobs, m):
    """
    List Scheduling (LS) algorithm.

    Args:
        jobs: List of job processing times
        m: Number of machines

    Returns:
        schedule: List of tuples (machine_id, start_time, end_time, job_id)
        makespan: Total completion time
    """
    # Initialize machine availability times
    machines = [0] * m
    schedule = []

    # Process jobs in order
    for job_id, job_time in enumerate(jobs):
        # Find machine that becomes available earliest
        earliest_machine = min(range(m), key=lambda i: machines[i])
        start_time = machines[earliest_machine]
        end_time = start_time + job_time

        # Assign job to this machine
        schedule.append((earliest_machine, start_time, end_time, job_id))
        machines[earliest_machine] = end_time

    makespan = max(machines)
    return schedule, makespan


def print_schedule(schedule, makespan, m):
    """Print the schedule in a readable format."""
    print(f"Number of machines: {m}")
    print(f"Makespan: {makespan}\n")

    # Group by machine
    for machine_id in range(m):
        machine_jobs = [s for s in schedule if s[0] == machine_id]
        print(f"Machine {machine_id}:")
        for _, start, end, job_id in machine_jobs:
            print(f"  Job {job_id}: [{start}, {end})")
        print()


# Example from the problem
jobs = [1, 2, 1, 4, 3, 2]
m = 3

schedule, makespan = list_scheduling(jobs, m)
print_schedule(schedule, makespan, m)

# Show the assignment sequence
print("Job assignment order:")
for machine_id, start, end, job_id in schedule:
    job_time = end - start
    print(f"Job {job_id} (time={job_time}) -> Machine {machine_id} at time {start}")
