#!/usr/bin/env python3

import io
import unittest.mock
import yaz


class ConfigurationPlugin(yaz.Plugin):
    """This is the documentation string for the ConfigurationPlugin"""

    choices = {
        "yes": True,
        "no": False,
        "unknown": None,
    }

    @yaz.task(choice__choices=["yes", "no", "unknown"])
    def required_choice(self, choice):
        """This is the documentation for the required_choice task"""
        return self.choices[choice]

    @yaz.task
    def one_line_doc_string(self):
        """This is the documentation for the one_line_doc_string task"""
        pass

    @yaz.task
    def multi_line_doc_string(self):
        """
        This is the documentation for the multi_line_doc_string task

        This is the long description, for example:
        bla bla,
        etc...
        """
        pass

    @yaz.task(choice__help="This is the documentation for the choice parameter of the parameter_help task")
    def parameter_help(self, choice):
        """This is the documentation for the parameter_help task"""
        pass


class Test(yaz.TestCase):
    def test_010_plugin_help(self):
        """Should show plugin help texts from docstring or configuration"""
        caller = self.get_caller([ConfigurationPlugin])

        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as stdout:
            with self.assertRaises(SystemExit):
                caller("--help")

            stdout.seek(0)
            output = stdout.read()

        print(output)

        self.assertRegex(output, r"This is the documentation string for the ConfigurationPlugin")
        self.assertRegex(output, r"This is the documentation for the required_choice task")
        self.assertRegex(output, r"This is the documentation for the one_line_doc_string task")
        self.assertRegex(output, r"This is the documentation for the parameter_help task")

        # we expect the first line of the the multi_line_doc_string task, not the rest
        self.assertRegex(output, r"This is the documentation for the multi_line_doc_string task")
        self.assertNotRegex(output, r"This is the long description, for example")

    def test_020_task_help__docstring(self):
        """Should show task help texts from docstring or configuration"""
        caller = self.get_caller([ConfigurationPlugin])

        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as stdout:
            with self.assertRaises(SystemExit):
                caller("multi-line-doc-string", "--help")

            stdout.seek(0)
            output = stdout.read()

        print(output)

        self.assertNotRegex(output, r"This is the documentation string for the ConfigurationPlugin")
        self.assertRegex(output, r"This is the documentation for the multi_line_doc_string task")
        self.assertRegex(output, r"This is the long description, for example")

    def test_030_task_help__parameter(self):
        """Should show task help texts from docstring or configuration"""
        caller = self.get_caller([ConfigurationPlugin])

        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as stdout:
            with self.assertRaises(SystemExit):
                caller("parameter-help", "--help")

            stdout.seek(0)
            output = stdout.read()

        print(output)

        self.assertNotRegex(output, r"This is the documentation string for the ConfigurationPlugin")
        self.assertRegex(output, r"This is the documentation for the parameter_help task")
        self.assertRegex(output, r"This is the documentation for the choice parameter of the\n.*parameter_help task")

    def test_040_choices_configuration(self):
        """Should accept predefined choices"""
        caller = self.get_caller([ConfigurationPlugin])

        # using available choice
        self.assertTrue(caller("required-choice", "yes"))

        # using unavailable choice
        with unittest.mock.patch("sys.stderr", new=io.StringIO()):
            with self.assertRaises(SystemExit):
                caller("required-choice", "unavailable")


if __name__ == "__main__":
    yaz.main()
