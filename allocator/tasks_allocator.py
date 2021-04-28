import pandas as pd
from collections import Counter


class TasksAllocator(object):
    def __init__(self):
        self.col_names = ["task_id", "type", "description", "version", "user"]

    @staticmethod
    def get_next_employee_typed(task_type, num_tasks_allocate, grouped_employees):
        for k, v in num_tasks_allocate.items():
            if k in grouped_employees[task_type] and v > 0:
                num_tasks_allocate[k] = v - 1
                return k

    @staticmethod
    def get_next_employee(num_tasks_allocate):
        for k, v in num_tasks_allocate.items():
            if v > 0:  # this indicates there is capacity available for employee
                num_tasks_allocate[k] = v - 1  # decrement capacity by 1
                return k

    @staticmethod
    def evenly_distribute_tasks(tasks_df, employees):
        total_tasks_count = len(tasks_df)
        employee_names = list(employees.keys())
        num_employees = len(employee_names)

        # The number of tasks each employee(user) should have
        per_user_tasks = total_tasks_count / num_employees
        num_tasks_allocate = {}  # this holds the capacity of each employee to be given unallocated tasks
        for employee in employee_names:
            # Subtract already allocated tasks from number of tasks each employee should have
            num_tasks_allocate[employee] = int(per_user_tasks - tasks_df['user'].value_counts()[employee])

        for index, row in tasks_df.iterrows():
            if row['user'] == 'None':
                # For each unallocated task, pick the next available employee and allocate
                row['user'] = TasksAllocator.get_next_employee(num_tasks_allocate)
        return tasks_df

    @staticmethod
    def correctly_distribute_tasks(tasks_df, employees):
        employee_type_counts = Counter(employees.values())
        per_employee_type_tasks = {}
        tasks_per_type = tasks_df['type'].value_counts()
        for v in employees.values():
            per_employee_type_tasks[v] = int(tasks_per_type[v] / employee_type_counts[v])

        grouped_employees = {}  # group employees by their type
        for employee_name, employee_type in employees.items():
            if employee_type in grouped_employees:
                grouped_employees[employee_type].append(employee_name)
            else:
                grouped_employees[employee_type] = [employee_name]

        correct_tasks = []  # determine which tasks are correctly allocated and shouldn't be modified
        for index, row in tasks_df.iterrows():
            if row['user'] != 'None' and row['user'] in grouped_employees[row['type']]:
                correct_tasks.append(row)
        correct_tasks_df = pd.DataFrame(correct_tasks)
        num_tasks_allocate = {}  # this holds the capacity of each employee to be given unallocated tasks
        for employee_name, employee_type in employees.items():
            num_tasks_allocate[employee_name] = int(per_employee_type_tasks[employee_type] - correct_tasks_df['user'].value_counts()[employee_name])

        for index, row in tasks_df.iterrows():
            if row['user'] == 'None' or row['user'] not in grouped_employees[row['type']]:
                row['user'] = TasksAllocator.get_next_employee_typed(row['type'], num_tasks_allocate, grouped_employees)

        return tasks_df
