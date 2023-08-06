import setuptools
import my_module

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name="my-module-r3ap3rpy",
    version=my_module.__version__,
    author="Dani",
    author_email="r3ap3rpy@gmail.com",
    description="Egy szimpla python module!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent" 
    ],
    python_requires='>=3.8.6'
)