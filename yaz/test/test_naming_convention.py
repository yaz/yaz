#!/usr/bin/env python3

import yaz


class NamingConventionThis_was__a_weirdMIXTure__(yaz.Plugin):
    @yaz.task
    def expected_class_name(self):
        return "naming-convention-this-was-a-weird-mixture"


class NamingConventionThisWasCamelCase(yaz.Plugin):
    @yaz.task
    def expected_class_name(self):
        return "naming-convention-this-was-camel-case"

    @yaz.task
    def this_was_underscored(self):
        return "this-was-underscored"

    @yaz.task
    def thisWasCamelCase(self):
        return "this-was-camel-case"

    @yaz.task
    def _this___was_also__underscored___(self):
        return "this-was-also-underscored"

    @yaz.task
    def required_arguments(self, this_was_underscored, thisWasCamelCase, _this___was_also__underscored___, D):
        return this_was_underscored, thisWasCamelCase, _this___was_also__underscored___, D

    @yaz.task
    def optional_arguments(self, this_was_underscored='A', thisWasCamelCase='B', _this___was_also__underscored___='C', D='D'):
        return this_was_underscored, thisWasCamelCase, _this___was_also__underscored___, D


class Test(yaz.TestCase):
    def test_010_plugin_name(self):
        """Should convert Plugin name to conform with naming conventions"""
        caller = self.get_caller([NamingConventionThis_was__a_weirdMIXTure__, NamingConventionThisWasCamelCase])
        self.assertEqual("naming-convention-this-was-a-weird-mixture", caller("naming-convention-this-was-a-weird-mixture"))
        self.assertEqual("naming-convention-this-was-camel-case", caller("naming-convention-this-was-camel-case", "expected-class-name"))

    def test_020_task_and_argument_name(self):
        """Should convert task name and argument name to conform with naming conventions"""
        caller = self.get_caller([NamingConventionThisWasCamelCase])
        self.assertEqual("this-was-underscored", caller("this-was-underscored"))
        self.assertEqual("this-was-camel-case", caller("this-was-camel-case"))
        self.assertEqual("this-was-also-underscored", caller("this-was-also-underscored"))
        self.assertEqual(("a", "b", "c", "d"), caller("required-arguments", "a", "b", "c", "d"))
        self.assertEqual(("A", "B", "C", "D"), caller("optional-arguments"))


if __name__ == "__main__":
    yaz.main()
