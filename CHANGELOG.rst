=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/>`_
and this project adheres to `Semantic Versioning <http://semver.org/>`_.

[Unreleased]
------------

1.0.3
-----

- Added: log messages when a task starts and ends, using info level
- Added: ``yaz.version`` containing the current version string
  `[#3] <https://github.com/boudewijn-zicht/yaz/issues/3>`_
- Changed: when no task is found to execute, exit with 1 (failure) instead of 0 (success)
- Fixed: arguments with underscores are now printed correctly in the generated
  ``--help`` output
  `[#7] <https://github.com/boudewijn-zicht/yaz/issues/7>`_
- Fixed: boolean and integer task return types should not be printed
  `[#8] <https://github.com/boudewijn-zicht/yaz/issues/8>`_

1.0.2
-----

- Added: ``CHANGELOG.rst``
- Changed: improvements to ``README.rst``

1.0.1
-----

- Added: ``yaz.Error class``.  When raised, the error message is
  printed (without the callstack) and the process exit code
  is set to 1.

1.0.0
-----

- Added: Initial stable release.
