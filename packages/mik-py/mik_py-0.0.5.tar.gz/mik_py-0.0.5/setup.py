import os
import setuptools
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setuptools.setup(
    name="mik_py",
    version="0.0.5",
    author="Mike",
    author_email="michaelrchung@gmail.com",
    description="A Python package containing the Eicar file to help test anti-malware or anti-virus software",
    long_description="Downloading this python package will also download the Eicar file as part of the python package https://www.eicar.org/download-anti-malware-testfile/./n/nThe Eicar file is a file used widely to test anti-malware software against malware and viruses. The Eicar file downloaded as part of this package is not malware but most anti-malware solutions will detect the Eicar file as malware or a virus and will trigger an alert. Please use this package with caution. This python package was created for testing purposes. Please use with caution as it will trigger alerts. ",
    long_description_content_type="text/markdown",
    #url="www.test.com",
    packages=find_packages(),
    include_package_data=True,
    packages_data={
        'eicar_py':['eicar.com'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)