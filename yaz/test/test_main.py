import unittest
import unittest.mock
import io

from yaz import main
from yaz.test.extension.singlefunction import say
from yaz.test.extension.errorfunction import yaz_error, return_boolean, return_integer


class TestMain(unittest.TestCase):
    def test_010(self):
        """Should run task, print, and exit"""
        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as stdout:
            with self.assertRaises(SystemExit) as context:
                main(["SCRIPT", "--message", "Echo!"], [say])

            # check exit code
            self.assertEqual(0, context.exception.code)

            # check stdout
            stdout.seek(0)
            self.assertEqual("Echo!\n", stdout.read())

    def test_020_no_tasks_available(self):
        """Should print help when no tasks are defined"""
        expected = """
usage: SCRIPT [-h] {} ...

optional arguments:
  -h, --help  show this help message and exit

subcommands:
  {}
""".lstrip()

        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as stdout:
            with self.assertRaises(SystemExit) as context:
                main(["SCRIPT"], [])

            # check exit code
            self.assertEqual(0, context.exception.code)

            # check stdout
            stdout.seek(0)
            self.assertEqual(expected, stdout.read())

    def test_030_print_help(self):
        """Should print help when not given arguments"""
        expected = """
usage: SCRIPT [-h] [--message MESSAGE]

optional arguments:
  -h, --help         show this help message and exit
  --message MESSAGE  defaults to message='Hello World!'
""".lstrip()

        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as stdout:
            with self.assertRaises(SystemExit) as context:
                main(["SCRIPT", "--help"], [say])

            # check exit code
            self.assertEqual(0, context.exception.code)

            # check stdout
            stdout.seek(0)
            self.assertEqual(expected, stdout.read())

    def test_040_task_raise_yaz_error(self):
        """Should exit with return code given by yaz.Error"""
        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as stdout:
            with self.assertRaises(SystemExit) as context:
                main(["SCRIPT", "--message", "There was a very specific error", "--return-code", "42"], [yaz_error])

            # check exit code
            self.assertEqual(42, context.exception.code)

            # check stdout
            stdout.seek(0)
            self.assertEqual("There was a very specific error\n", stdout.read())

    def test_050_task_returns_integer(self):
        """Should exit with task integer return value"""
        for value, code in [(-10, 246), (0, 0), (1, 1), (42, 42), (255, 255), (256, 0), (257, 1)]:
            with self.assertRaises(SystemExit) as context:
                main(["SCRIPT", str(value)], [return_integer])
            self.assertEqual(code, context.exception.code)

    def test_060_task_returns_boolean(self):
        """Should exit with task boolean return value"""
        with self.assertRaises(SystemExit) as context:
            main(["SCRIPT", "--value"], [return_boolean])
        self.assertEqual(0, context.exception.code)

        with self.assertRaises(SystemExit) as context:
            main(["SCRIPT", "--no-value"], [return_boolean])
        self.assertEqual(1, context.exception.code)
