from setuptools import setup

setup(name='dhaffner',
      version='0.1',
      description='Some Python utility modules.',
      url='http://github.com/dhaffner/dhaffner.py',
      author='Dustin Haffner',
      author_email='dh@xix.org',
      license='MIT',
      packages=['dhaffner'],
      install_requires=[
          'six'
      ],
      zip_safe=False)
