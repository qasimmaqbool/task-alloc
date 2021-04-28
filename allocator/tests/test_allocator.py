import pandas as pd
import unittest
from allocator.tasks_allocator import TasksAllocator


class TestExample(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.alloc = TasksAllocator()

    def test_evenly_allocate(self):
        tasks = pd.DataFrame([['1', 't1', 'emp1'], ['2', 't2', 'emp1'], ['3', 't1', 'emp2'], ['4', 't2', 'None'],
                              ['5', 't1', 'None'], ['6', 't2', 'emp3']], columns=['task_id', 'type', 'user'])
        employees = {'emp1': 't1', 'emp2': 't2', 'emp3': 't1'}
        res_df = self.alloc.evenly_distribute_tasks(tasks, employees)
        self.assertEqual(len(res_df), 6)

        emp1_tasks_list = res_df[res_df['user'] == 'emp1']
        self.assertEqual(len(emp1_tasks_list), 2)

        emp2_tasks_list = res_df[res_df['user'] == 'emp2']
        self.assertEqual(len(emp2_tasks_list), 2)

        emp3_tasks_list = res_df[res_df['user'] == 'emp3']
        self.assertEqual(len(emp3_tasks_list), 2)

    def test_correctly_allocate(self):
        tasks = pd.DataFrame([['1', 't1', 'emp1'], ['2', 't2', 'None'], ['3', 't1', 'emp2'], ['4', 't1', 'emp3'],
                              ['5', 't1', 'None'], ['6', 't2', 'emp2'], ['7', 't1', 'None'], ['8', 't1', 'None']],
                             columns=['task_id', 'type', 'user'])
        employees = {'emp1': 't1', 'emp2': 't2', 'emp3': 't1'}
        res_df = self.alloc.correctly_distribute_tasks(tasks, employees)
        print(res_df)
        self.assertEqual(len(res_df), 8)

        emp1_tasks_list = res_df[res_df['user'] == 'emp1']
        self.assertEqual(len(emp1_tasks_list), 3)

        emp2_tasks_list = res_df[res_df['user'] == 'emp2']
        self.assertEqual(len(emp2_tasks_list), 2)

        emp3_tasks_list = res_df[res_df['user'] == 'emp3']
        self.assertEqual(len(emp3_tasks_list), 3)


if __name__ == '__main__':
    unittest.main()
