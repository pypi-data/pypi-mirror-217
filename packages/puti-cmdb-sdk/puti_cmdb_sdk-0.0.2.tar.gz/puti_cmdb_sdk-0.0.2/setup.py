from distutils.core import setup
from distutils.extension import Extension

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name="puti_cmdb_sdk",
  version="0.0.2",
  author="jack",
  author_email="jack@example.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/sampleproject",
  packages=[
    'cmdb_sdk',
  ],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)