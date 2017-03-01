from setuptools import setup

setup(name="yaz",
      packages=["yaz"],
      version="1.0.0",
      description="A scripting tool",
      author="Boudewijn Schoon",
      author_email="yaz@frayja.com",
      url="https://github.com/boudewijn-zicht/yaz",
      license="MIT",
      zip_safe=False,
      test_suite="nose.collector",
      tests_require=["nose"],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6"
      ])
