#!/usr/bin/env python3

from setuptools import setup, find_packages
import re

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version():
    with open('captcha/__init__.py', 'r') as f:
        return re.search(r'__version__ = ["\'](.*?)["\']', f.read()).group(1)


setup(name='captchaai',
      version=get_version(),
      description='Python module for easy integration with captchaai.com API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/captchaai-developers/captchaai-python/',
      install_requires=['requests'],
      author='captchaai.com developers',
      author_email='dev@captchaai.com',
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      test_suite='tests')