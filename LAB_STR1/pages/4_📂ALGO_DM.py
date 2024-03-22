import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
from math import gcd
from functools import reduce


def lcm(a, b):
    return a * b // gcd(a, b)


def lcm_for_periods(periods):
    return reduce(lcm, periods)


def is_feasible(processes):
    return sum(burst_time / period for _, period, burst_time, _ in processes) <= 1


def calculate_dm_intervals(processes, total_time):
    processes.sort(key=lambda x: x[3])  # Trier par deadline
    intervals = {p[0]: [] for p in processes}
    remaining_burst_times = {p[0]: 0 for p in processes}
    current_process_index = None

    for time in range(total_time):
        for i, (process_id, period, burst_time, deadline) in enumerate(processes):
            if time % period == 0:
                if remaining_burst_times[process_id] > 0:  # Si le processus manque sa deadline
                    st.write(f"Deadline missed for {process_id}")
                    return None
                remaining_burst_times[process_id] = burst_time

            if remaining_burst_times[process_id] > 0:
                if current_process_index is None or deadline < processes[current_process_index][3]:
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

    st.write("Intervals Calculated:", intervals)
    return intervals


def display_gantt_chart(processes, intervals):
    gantt_data = []
    for process_id, _, _, _ in sorted(processes, key=lambda x: x[0]):
        for interval in intervals[process_id]:
            start, finish = interval
            gantt_data.append(dict(Task=process_id, Start=start, Finish=finish))

    fig = ff.create_gantt(gantt_data, index_col='Task', show_colorbar=True, group_tasks=True)

    total_duration = max([max(interval[-1] for interval in intervals[pid]) for pid, _, _, _ in processes])
    st.write("Total Duration:", total_duration)

    # Ajout des lignes et annotations pour les périodes et deadlines
    for process_id, period, _, deadline in processes:
        # Lignes pour la période
        for time in range(0, total_duration + 1, period):
            fig.add_shape(type='line', x0=time, y0=0, x1=time, y1=len(processes) + 1,
                          line=dict(color="LightSeaGreen", width=2, dash="dashdot"))
            fig.add_annotation(x=time, y=len(processes) + 1, text=f'P{process_id}',
                               showarrow=False, yshift=10)

        # Lignes pour la deadline
        for time in range(0, total_duration + 1, period):
            if deadline < period:
                deadline_time = time + deadline
                if deadline_time <= total_duration:
                    fig.add_shape(type='line', x0=deadline_time, y0=0, x1=deadline_time, y1=len(processes) + 1,
                                  line=dict(color="Red", width=2, dash="dot"))
                    fig.add_annotation(x=deadline_time, y=len(processes) + 1, text=f'D{process_id}',
                                       showarrow=False, yshift=-10)

    x_ticks = sorted(set(time for task in gantt_data for time in [task['Start'], task['Finish']]))
    x_ticks_str = [str(time) for time in x_ticks]

    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            tickvals=x_ticks,
            ticktext=x_ticks_str,
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
    st.title("Deadline Monotonic Scheduling Algorithm")

    num_processes = st.number_input("Enter the number of processes", min_value=1, value=3)
    processes = []

    for i in range(num_processes):
        process_id = st.text_input(f"Process {i + 1} ID", f"P{i + 1}")
        period = st.number_input(f"Period for Process {process_id}", min_value=1, value=10)
        burst_time = st.number_input(f"Burst Time for Process {process_id}", min_value=1, value=1)
        deadline = st.number_input(f"Deadline for Process {process_id}", min_value=1, value=period)
        processes.append((process_id, period, burst_time, deadline))

    if st.button("Run DM"):
        if is_feasible(processes):
            total_time = lcm_for_periods([p[1] for p in processes])
            st.write(f"Total simulation time (LCM of periods): {total_time}")

            # Affichage du tableau récapitulatif
            st.write("Entered Process Details:")
            summary_table = pd.DataFrame(processes, columns=['Process ID', 'Period', 'Burst Time', 'Deadline'])
            st.table(summary_table)

            intervals = calculate_dm_intervals(processes, total_time)
            if intervals:
                display_gantt_chart(processes, intervals)

                feasibility_value1 = sum(burst_time / period for _, period, burst_time, _ in processes)
                feasibility_value = sum(burst_time / period for _, period, burst_time, _ in processes) * 100
                st.write(f"nous avons la valeur: {feasibility_value1:.2f} <= 1 donc un système ordonnançable avec un taux d'utilisation de {feasibility_value:.2f} %")
            else:
                st.write("Unable to meet deadlines with given constraints.")
        else:
            st.write("System is not feasible under Deadline Monotonic Scheduling.")


if __name__ == "__main__":
    main()
