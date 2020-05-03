import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruben-snake-cmd",
    version="0.2.0",
    author="Ruben Dougall",
    # author_email="author@example.com",
    description="Simple utility functions for command-line applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruben9922/snake-cmd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['ruben-snake-cmd=snake_cmd:main'],
    },
)
