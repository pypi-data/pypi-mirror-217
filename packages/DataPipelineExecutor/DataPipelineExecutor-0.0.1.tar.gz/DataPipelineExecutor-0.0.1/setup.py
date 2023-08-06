from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='DataPipelineExecutor',
    version='0.0.1',
    description='A package to execute Copy and Stored Procedure tasks on data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=["DataPipelineExecutor"],
    package_dir={'':'src'},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)