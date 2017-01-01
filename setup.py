from setuptools import setup

setup(name='yaz',
      version='1.0.0-beta.1',
      description='A scripting tool',
      author='Boudewijn Schoon',
      author_email='yaz@frayja.com',
      license='MIT',
      packages=['yaz'],
      install_requires=['jinja2'],
      zip_safe=False)
