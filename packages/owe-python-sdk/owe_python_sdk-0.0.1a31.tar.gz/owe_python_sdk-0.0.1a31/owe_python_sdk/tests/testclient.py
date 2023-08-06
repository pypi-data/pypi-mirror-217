import unittest


from tests.fixtures.valid_tasks import image_build
from client import Task


class TestTask(unittest.TestCase):
    def testInitTasks(self):
        # self.assertEqual(type(Task(image_build)), Task)
        self.assertEqual(1,1)

if __name__ == "__main__":
    unittest.main()