import sys
import time
from unittest import TestCase
from unittest.mock import patch

from project.task1 import main as task1_main
from project.task2 import main as task2_main


class TestTask1(TestCase):
    def setUp(self):
        self.files = ['link1', 'link2', 'link3', 'link4', 'link5']

    def tearDown(self):
        pass

    @patch('builtins.input', return_value='exit')
    def test_exit(self, *args):
        task1_main(self.files)
        output = sys.stdout.getvalue()
        self.assertEqual('Exit', output)

    @patch('builtins.input', return_value='not_support')
    def test_not_supported_command(self, *args):
        task1_main(self.files)
        output = sys.stdout.getvalue().strip()
        self.assertEqual('Command not supported', output)

    @patch('builtins.input', return_value='test invalid command')
    def test_invalid_command(self, *args):
        task1_main(self.files)
        output = sys.stdout.getvalue().strip()
        self.assertEqual('Invalid command', output)


class TestTask2(TestCase):
    def setUp(self):
        self.files = ['link1', 'link2', 'link3', 'link4', 'link5']

    def tearDown(self):
        pass

    def test_work_10_processes(self):
        start_time = time.time()
        task2_main(self.files, 10)
        result_time = time.time() - start_time
        print(result_time)
        self.assertTrue(result_time < 7)

    def test_work_4_processes(self):
        start_time = time.time()
        task2_main(self.files, 4)
        result_time = time.time() - start_time
        print(result_time)
        self.assertTrue(result_time < 12)

    def test_work_1_process(self):
        start_time = time.time()
        task2_main(self.files, 1)
        result_time = time.time() - start_time
        print(result_time)
        self.assertTrue(result_time < 27)
