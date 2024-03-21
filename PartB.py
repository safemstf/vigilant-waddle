import numpy as np
import math
import random

# operation times for R3
operation_times_r3 = np.array([
    [3, 6],  # Job 1
    [10, 1],  # Job 2
    [3, 2],
    [2, 4],
    [8, 8]
])


# main simulation
def simulated_sa(J, N, M, t=1000, iteration=400, custom_times=None):
    # custom times for R4 and R5
    if custom_times is not None:
        operation_times = custom_times
    # default to R3
    else:
        operation_times = np.random.randint(5, 56, size=(J, N))

    def operation_time(job_id, operation_num):
        return operation_times[job_id - 1, operation_num - 1]

    def allocate_operations_to_machines(job_schedule, J, N, M):
        opt_schedule = []
        start_times = [0] * M
        last_job_end_times = [0] * J

        for job_id in job_schedule:
            for operation_num in range(1, N + 1):
                mach = (operation_num - 1) % M
                start_time = max(start_times[mach], last_job_end_times[job_id - 1])
                operation_duration = operation_time(job_id, operation_num)
                end_time = start_time + operation_duration
                opt_schedule.append((f"J{job_id}{operation_num}", start_time, end_time, mach))

                start_times[mach] = end_time
                last_job_end_times[job_id - 1] = end_time

        return opt_schedule

    def comp_makespan(opt_schedule):
        makespan = max([end for _, _, end, _ in opt_schedule])
        return makespan

    def successor(job_schedule):
        new_schedule = job_schedule.copy()
        idx1, idx2 = np.random.choice(len(new_schedule), 2, replace=False)
        new_schedule[idx1], new_schedule[idx2] = new_schedule[idx2], new_schedule[idx1]

        return new_schedule

    current_job_schedule = np.random.permutation(np.arange(1, J + 1))
    initial_opt_schedule = allocate_operations_to_machines(current_job_schedule, J, N, M)
    initial_makespan = comp_makespan(initial_opt_schedule)

    current_makespan = initial_makespan
    for i in range(iteration):
        next_job_schedule = successor(current_job_schedule)
        next_opt_schedule = allocate_operations_to_machines(next_job_schedule, J, N, M)
        next_makespan = comp_makespan(next_opt_schedule)
        deltaE = next_makespan - current_makespan

        if deltaE < 0 or math.exp(-deltaE / t) > random.random():
            current_job_schedule = next_job_schedule
            current_makespan = next_makespan

        t *= 0.80  # Cool down

    return initial_makespan, current_makespan


# Running Scenario for R3
J, N, M = 5, 2, 2
initial_makespan_r3, final_makespan_r3 = simulated_sa(J, N, M, custom_times=operation_times_r3)
print(f"R3 Initial Makespan: {initial_makespan_r3}, Final Makespan: {final_makespan_r3}, Optimal Makespan: 27")

# Running scenario for R4
J, N, M = 50, 3, 5
initial_makespan_r4, final_makespan_r4 = simulated_sa(J, N, M)
print(f"R4 Initial Makespan: {initial_makespan_r4}, Final Makespan: {final_makespan_r4}")

# Running Scenario for R5
J, N, M = 50, 5, 3
initial_makespan_r5, final_makespan_r5 = simulated_sa(J, N, M)
print(f"R5 Initial Makespan: {initial_makespan_r5}, Final Makespan: {final_makespan_r5}")
