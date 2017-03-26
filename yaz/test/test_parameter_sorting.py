#!/usr/bin/env python3

import io
import unittest.mock
import yaz


@yaz.task
def parameter_sorting(c, b, a, f="F", e="E", d="D"):
    return [c, b, a, d, e, f]


class Test(yaz.TestCase):
    def test_010(self):
        """Test parameter sorting
    
        There are required and non-required arguments, the required arguments are
        positional and hence may *not* be sorted.  However, the required arguments
        *should* be sorted as this makes the API cleaner.
        """
        caller = self.get_caller([parameter_sorting])
        self.assertEqual(["A", "B", "C", "D", "E", "F"], caller("A", "B", "C", "-d", "D", "-e", "E", "-f", "F"))

    def test_020(self):
        """Test parameter sorting in the --help"""
        caller = self.get_caller([parameter_sorting])

        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as stdout:
            with self.assertRaises(SystemExit):
                caller("--help")

            stdout.seek(0)
            output = stdout.read()

        print(output)

        # the required arguments should be in the original order C B A
        self.assertRegex(output, r"c b a")

        # the non-required arguments should be ordered alphabetically
        self.assertRegex(output, r"\[-d D\] \[-e E\] \[-f F\]")


if __name__ == "__main__":
    yaz.main()
