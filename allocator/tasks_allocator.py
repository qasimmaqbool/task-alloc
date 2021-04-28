

class TasksAllocator(object):
    def __init__(self):
        self.col_names = ["task_id", "type", "description", "version", "user"]

    @staticmethod
    def get_next_employee(num_tasks_allocate):
        for k, v in num_tasks_allocate.items():
            if v > 0:
                num_tasks_allocate[k] = v - 1
                return k

    @staticmethod
    def evenly_distribute_tasks(tasks_df, employees):
        total_tasks_count = len(tasks_df)
        employee_names = list(employees.keys())
        num_employees = len(employee_names)
        per_user_tasks = total_tasks_count / num_employees
        num_tasks_allocate = {}
        for employee in employee_names:
            num_tasks_allocate[employee] = int(per_user_tasks - tasks_df['user'].value_counts()[employee])

        for index, row in tasks_df.iterrows():
            if row['user'] == 'None':
                row['user'] = TasksAllocator.get_next_employee(num_tasks_allocate)

        return tasks_df
