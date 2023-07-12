from setuptools import setup, find_packages
from pkg_resources import parse_requirements
from robokami import robokami_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="robokami-py",
    version=robokami_version,
    author="Robokami",
    description="Robokami Client Python SDK",
    packages=find_packages(),
    install_requires=["sseclient_py==1.7.2"],
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Tideseed/robokami-py",
    license="Apache License 2.0",
    # classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # Install requires get from requirements.txt
    # install_requires=[
    #     str(r.req) for r in parse_requirements("requirements.txt", session=False)
    # ],
)


## To create a requirements.txt file from the project: pipreqs . --force
## To install from requirements.txt: pip install -r requirements.txt OR uncomment the install_requires line above
