#!/usr/bin/env python3

# in the context of nosetests `import yaz` is not available
try:
    from yaz import yaz
except ImportError:
    import yaz

class ConfigurationPlugin(yaz.Plugin):
    """TODO: This is the documentation string for the ConfigurationPlugin"""

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
    def task_doc_string(self):
        """This is the documentation for the doc_string task"""
        # todo: needs a unit test
        pass

    @yaz.task(choice__help="This is the documentation for the choice parameter")
    def parameter_help(self, choice):
        # todo: needs a unit test
        pass

if __name__ == "__main__":
    yaz.main()
