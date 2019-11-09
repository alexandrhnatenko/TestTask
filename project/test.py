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

    @patch('builtins.input', side_effect=['upload', 'exit'], )
    def test_upload_command_without_parameter(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        self.assertEqual('Invalid command', output[0])

    @patch('builtins.input', side_effect=['upload 4', 'exit'])
    def test_upload_command_with_parameter(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        self.assertEqual('Invalid command', output[0])

    @patch('builtins.input', side_effect=['stop', 'exit'])
    def test_stop_command_without_parameter(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        self.assertEqual('Invalid command', output[0])

    @patch('builtins.input', side_effect=['stop 3', 'exit'])
    def test_stop_command_with_parameter(self, *args):
        with Capturing() as output:
            task1_main(self.files)
        self.assertEqual('Invalid command', output[0])


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
