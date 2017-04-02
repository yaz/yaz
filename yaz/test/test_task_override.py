#!/usr/bin/env python3

import yaz


class ArgsTaskOverride(yaz.BasePlugin):
    @yaz.task
    def main(self, pos1: str, pos2: str):
        return [pos1, pos2]


class ArgsTaskOverride(ArgsTaskOverride):
    @yaz.task
    def main(self, pos1: str, *args):
        return super().main(pos1, *args)


class KwargsTaskOverride(yaz.BasePlugin):
    @yaz.task
    def main(self, key1: str, key2: str):
        return [key1, key2]


class KwargsTaskOverride(KwargsTaskOverride):
    @yaz.task
    def main(self, key1: str, **kwargs):
        return super().main(key1, **kwargs)


class MixedTaskOverride(yaz.BasePlugin):
    """water-base-plugin"""

    @yaz.task
    def main(self, pos1: str, pos2: str, pos3: str, pos_or_key1: str = "POS_OR_KEY1", pos_or_key2: str = "POS_OR_KEY2", pos_or_key3: str = "POS_OR_KEY3", *, key1: str = "KEY1", key2: str = "KEY2", key3: str = "KEY3"):
        """required from water-base-plugin"""
        return [pos1, pos2, pos3, pos_or_key1, pos_or_key2, pos_or_key3, key1, key2, key3]


class MixedTaskOverride(MixedTaskOverride):
    """water-plugin"""

    @yaz.task
    def main(self, pos1: str, pos2: str, pos_or_key1: str = "POS_OR_KEY1", pos_or_key2: str = "alt-POS_OR_KEY2", *, key1: str = "KEY1", key2: str = "alt-KEY2", extra2: str = "EXTRA2", **kwargs):
        """required from water-base"""
        return super().main(pos1, pos2, pos_or_key1=pos_or_key1, pos_or_key2=pos_or_key2, key1=key1, key2=key2, **kwargs) + [extra2]


class MixedTaskOverride(MixedTaskOverride):
    """water-custom-plugin"""

    @yaz.task
    def main(self, pos1: str, pos_or_key1: str = "alt-POS_OR_KEY1", *, key1: str = "alt-KEY1", extra1: str = "EXTRA1", **kwargs):
        """required from water-custom-plugin"""
        return super().main(pos1, pos_or_key1=pos_or_key1, key1=key1, **kwargs) + [extra1]


class Test(yaz.TestCase):
    def test_010_args(self):
        """*args should not be allowed in a task definition"""
        with self.assertRaisesRegex(RuntimeError, "Task .* contains an unsupported parameter \"[*]args\""):
            self.get_caller([ArgsTaskOverride])

    def test_020_kwargs(self):
        """Test task override with **kwargs"""
        caller = self.get_caller([KwargsTaskOverride])
        self.assertEqual(["A", "B"], caller("A", "B"))

    def test_030_mixed(self):
        """Should be able to use *args and **kwargs to get parameters from super classes"""
        caller = self.get_caller([MixedTaskOverride])

        expected = ["console-POS1", "console-POS1", "console-POS3",
                    "alt-POS_OR_KEY1", "alt-POS_OR_KEY2", "POS_OR_KEY3",
                    "alt-KEY1", "alt-KEY2", "KEY3", "EXTRA2", "EXTRA1"]
        self.assertEqual(expected, caller("console-POS1", "console-POS1", "console-POS3"))

        expected = ["console-POS1", "console-POS1", "console-POS3",
                    "console-POS_OR_KEY1", "console-POS_OR_KEY2", "console-POS_OR_KEY3",
                    "console-KEY1", "console-KEY2", "console-KEY3",
                    "console-EXTRA2", "console-EXTRA1"]
        self.assertEqual(expected,
                         caller(
                             "console-POS1",
                             "console-POS1",
                             "console-POS3",
                             "--pos-or-key1", "console-POS_OR_KEY1",
                             "--pos-or-key2", "console-POS_OR_KEY2",
                             "--pos-or-key3", "console-POS_OR_KEY3",
                             "--key1", "console-KEY1",
                             "--key2", "console-KEY2",
                             "--key3", "console-KEY3",
                             "--extra1", "console-EXTRA1",
                             "--extra2", "console-EXTRA2"))


if __name__ == "__main__":
    yaz.main()
