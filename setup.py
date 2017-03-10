import os
import setuptools
import sys

version = "1.0.2"

if sys.argv[-1] == "tag":
    os.system("git tag -a {} -m \"Release {}\"".format(version, version))
    os.system("git push origin {}".format(version))
    sys.exit()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now")
    sys.exit()

setuptools.setup(name="yaz",
      packages=["yaz"],
      version=version,
      description="A scripting tool",
      author="Boudewijn Schoon",
      author_email="yaz@frayja.com",
      url="https://github.com/boudewijn-zicht/yaz",
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
