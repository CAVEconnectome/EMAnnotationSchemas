from setuptools import setup, find_packages
import re
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("requirements.txt", "r") as f:
    required = f.read().splitlines()

with open("test_requirements.txt", "r") as f:
    test_required = f.read().splitlines()

with open("requirements_service.txt", "r") as f:
    required_service = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    version=find_version("emannotationschemas", "__init__.py"),
    name="emannotationschemas",
    description="a service for storing arbitrary annotation data "
    "on EM volumes stored in a cloud volume ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Forrest Collman",
    author_email="forrestc@alleninstitute.org",
    url="https://github.com/fcollman/EMAnnotationSchemas",
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    setup_requires=["pytest-runner"],
    tests_require=test_required + required_service,
    extras_require={"service": required_service},
)
