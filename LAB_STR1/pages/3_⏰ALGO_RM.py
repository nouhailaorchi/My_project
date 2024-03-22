import streamlit as st
import pandas as pd
from plotly import figure_factory as ff
import functools


def is_feasible(processes):
    return sum(burst_time / period for _, period, burst_time, _ in processes) <= 1

def _lcm(x, y):
    if x > y:
        greater = x
    else:
        greater = y

    while True:
        if greater % x == 0 and greater % y == 0:
            lcm = greater
            break
        greater += 1

    return lcm

def lcm_for_periods(periods):
    return functools.reduce(_lcm, periods)
def calculate_rm_intervals(processes, total_time):
    processes.sort(key=lambda x: x[1])  # Trier par période
    intervals = {p[0]: [] for p in processes}
    remaining_burst_times = {p[0]: 0 for p in processes}
    current_process_index = None

    for time in range(total_time):
        for i, (process_id, period, burst_time, deadline) in enumerate(processes):
            if time % period == 0:
                if remaining_burst_times[process_id] > 0:  # Si le processus manque sa deadline
                    print(f"Deadline missed for {process_id}")
                    return None
                remaining_burst_times[process_id] = burst_time

            if remaining_burst_times[process_id] > 0:
                if current_process_index is None or period < processes[current_process_index][1]:
                    current_process_index = i

        if current_process_index is not None:
            current_process_id = processes[current_process_index][0]
            remaining_burst_times[current_process_id] -= 1
            if not intervals[current_process_id] or intervals[current_process_id][-1][1] != time:
                intervals[current_process_id].append([time, time + 1])
            else:
                intervals[current_process_id][-1][1] += 1

            if remaining_burst_times[current_process_id] == 0:
                current_process_index = None

    print("Intervals Calculated:", intervals)
    return intervals


def display_gantt_chart(processes, intervals):
    gantt_data = []
    for process_id, _, _, _ in sorted(processes, key=lambda x: x[0]):
        for interval in intervals[process_id]:
            start, finish = interval
            gantt_data.append(dict(Task=process_id, Start=start, Finish=finish))

    fig = ff.create_gantt(gantt_data, index_col='Task', show_colorbar=True, group_tasks=True)

    total_duration = max([max(interval[-1] for interval in intervals[pid]) for pid, _, _, _ in processes])
    print("Total Duration:", total_duration)
    x_ticks = sorted(set(time for task in gantt_data for time in [task['Start'], task['Finish']]))

    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            tickvals=x_ticks,

        ),
        yaxis=dict(
            showgrid=True,
        ),
        title_text='Gantt Chart',
        xaxis_title='Time Slots',
        yaxis_title='Tasks',
        xaxis_type='linear',
    )
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.title("Rate Monotonic Scheduling Algorithm")

    num_processes = st.number_input("Enter the number of processes", min_value=1, value=3)
    processes = []

    for i in range(num_processes):
        process_id = st.text_input(f"Process {i + 1} ID", f"P{i + 1}")
        period = st.number_input(f"Period for Process {process_id}", min_value=1, value=10)
        burst_time = st.number_input(f"Burst Time for Process {process_id}", min_value=1, value=1)
        deadline = st.number_input(f"Deadline for Process {process_id}", min_value=1, value=period)
        processes.append((process_id, period, burst_time, deadline))

    if st.button("Run RM"):
        if is_feasible(processes):
            total_time = lcm_for_periods([p[1] for p in processes])
            st.write(f"Total simulation time (LCM of periods): {total_time}")

            # Afficher le tableau récapitulatif
            st.write("Entered Process Details:")
            summary_table = pd.DataFrame(processes, columns=['Process ID', 'Period', 'Burst Time', 'Deadline'])
            st.table(summary_table)

            intervals = calculate_rm_intervals(processes, total_time)
            if intervals:
                display_gantt_chart(processes, intervals)
            else:
                st.write("Unable to meet deadlines with given constraints.")
        else:
            st.write("System is not feasible under Rate Monotonic Scheduling.")


if __name__== "__main__":
    main()