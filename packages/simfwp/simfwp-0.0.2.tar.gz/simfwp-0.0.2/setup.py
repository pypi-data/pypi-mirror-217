from setuptools import setup, find_packages

setup(
    name="simfwp",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        # List your project dependencies here, e.g.
        # "numpy>=1.0",
        # "pandas>=1.0",
    ],
    entry_points={
        "console_scripts": [
            # If your project has command-line scripts, add their entry points here, e.g.
            # "my_script=my_package.my_module:main",
        ],
    },
    python_requires=">=3.11",
    # Add metadata about your project
    author="Jacob Meyers",
    author_email="jakejem@outlook.com",
    description="Makes Reading, Writing, Adding to files easier.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
		"Programming Language :: Python :: 3.11",
    ],
)
