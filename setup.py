import os
import setuptools
import sys

with open("yaz/version.py") as file:
    globals = {}
    exec(file.read(), globals)
    version = globals["__version__"]

if sys.argv[-1] == "tag":
    os.system("git tag -a {} -m \"Release {}\"".format(version, version))
    os.system("git push origin {}".format(version))
    sys.exit()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

setuptools.setup(name="yaz",
      packages=["yaz"],
      version=version,
      description="A scripting tool",
      author="Boudewijn Schoon",
      author_email="boudewijnschoon@gmail.com",
      url="https://github.com/yaz/yaz",
      license="MIT",
      zip_safe=False,
      test_suite="nose.collector",
      tests_require=["nose", "coverage"],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6"
      ])
