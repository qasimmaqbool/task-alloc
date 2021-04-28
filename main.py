import ast
import pandas as pd
from allocator import tasks_allocator

e = tasks_allocator.TasksAllocator()

tasks_data_filename = 'coding_test/tasks.csv'
employees_data_filename = 'coding_test/employees.txt'

tasks_df = pd.read_csv(tasks_data_filename)
with open(employees_data_filename) as employees_file:
    employees = ast.literal_eval(employees_file.read())

evenly_allocated_tasks = e.evenly_distribute_tasks(tasks_df, employees)

correctly_allocated_tasks = e.correctly_distribute_tasks(tasks_df, employees)

