# import setuptools
#
# with open("README.md", "r") as fh:
#   long_description = fh.read()
#
# setuptools.setup(
#   name="jacktest",
#   version="0.0.2",
#   author="jack",
#   author_email="jack@example.com",
#   description="A small example package",
#   long_description=long_description,
#   long_description_content_type="text/markdown",
#   url="https://github.com/pypa/sampleproject",
#   packages=setuptools.find_packages(),
#   classifiers=[
#   "Programming Language :: Python :: 3",
#   "License :: OSI Approved :: MIT License",
#   "Operating System :: OS Independent",
#   ],
# )


from distutils.core import setup
from setuptools import find_packages
with open("README.md", "r") as fh:
  long_description = fh.read()

setup(name='jacktest',  # 包名
      version='0.0.3',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='jack',
      author_email='jack@example.com',
      url='https://github.com/pypa/sampleproject',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )