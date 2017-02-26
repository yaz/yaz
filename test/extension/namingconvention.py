#!/usr/bin/env python3

import yaz


class ThisWasCamelCase(yaz.Plugin):
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


if __name__ == "__main__":
    yaz.main()
