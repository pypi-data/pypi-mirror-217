import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="degiroxxx",
    version="0.0.1",
    author="xxx",
    author_email="xxxxxxxxxxxxxxxxxxxx@gmail.com",
    description="Degiroxxx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gregory798/degiroxxx/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)