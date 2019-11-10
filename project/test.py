import sys
import time
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from project.task1 import main as task1_main
from project.task2 import main as task2_main


# for reading function output
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def generate_input(list_commands, list_intervals):
    for i in range(len(list_commands)):
        time.sleep(list_intervals[i])
        yield list_commands[i]


class TestTask1(TestCase):
    def setUp(self):
        self.files = ['link1', 'link2', 'link3', 'link4', 'link5']

    def tearDown(self):
        pass

    @patch('builtins.input', return_value='exit')
    def test_exit(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        self.assertEqual('Exit', output[0])

    @patch('builtins.input', side_effect=['not_support', 'exit'])
    def test_not_supported_command(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        self.assertEqual('Command not supported', output[0])

    @patch('builtins.input', side_effect=['test invalid command', 'exit'])
    def test_invalid_command(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        self.assertEqual('Invalid command', output[0])

    @patch('builtins.input',
           side_effect=generate_input(['upload', 'exit'], [0.1, 26]))
    def test_upload_command_without_parameter(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        correct_output = ['Done: 0, Error: 0, Total:5',
                          'Done: 5, Error: 0, Total:5',
                          'Exit']
        self.assertEqual(correct_output, output)

    @patch('builtins.input',
           side_effect=generate_input(['upload 4', 'exit'], [0.1, 11]))
    def test_upload_command_with_parameter(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        correct_output = ['Done: 0, Error: 0, Total:5',
                          'Done: 5, Error: 0, Total:5',
                          'Exit']
        self.assertEqual(correct_output, output)

    @patch('builtins.input',
           side_effect=generate_input(['upload 4', 'stop', 'exit'],
                                      [0.1, 1, 1]))
    def test_stop_command_without_parameter(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        correct_output = ['Done: 0, Error: 0, Total:5',
                          'Done: 0, Error: 5, Total:5',
                          'Done: 0, Error: 5, Total:5',
                          'Exit']
        self.assertEqual(correct_output, output)

    @patch('builtins.input',
           side_effect=generate_input(['upload 5', 'stop 1', 'stop 3', 'exit'],
                                      [0.1, 1, 1, 4]))
    def test_stop_command_with_parameter(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        correct_output = ['Done: 0, Error: 0, Total:5',
                          'Done: 0, Error: 1, Total:5',
                          'Done: 0, Error: 2, Total:5',
                          'Done: 3, Error: 2, Total:5',
                          'Exit']
        self.assertEqual(correct_output, output)


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
