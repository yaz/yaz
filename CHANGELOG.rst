=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

[Unreleased]
------------

- Added: log messages when a task starts and ends, using info level
- Changed: when no task is found to execute, exit with 1 (failure) instead of 0 (success)
- Fixed: arguments with underscores are now printed correctly in the generated
  ``--help`` output [#7](https://github.com/boudewijn-zicht/yaz/issues/7)
- Fixed: boolean and integer task return types should not be printed
  [#8](https://github.com/boudewijn-zicht/yaz/issues/8)

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
