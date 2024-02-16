import codecs
import os

from setuptools import find_packages, setup


def read(name: str):
    file_path = os.path.join(os.path.dirname(__file__), name)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-schema",
    use_scm_version=True,
    author="Brett Dawidowski",
    author_email="brett@codedawi.com",
    license="MIT",
    url="https://github.com/codedawi/pytest-schema",
    description="👍 Validate return values against a schema-like object in testing",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    python_requires="!=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=[
        "pytest>=3.5.0",
        "schema>=0.7.0",
    ],
    setup_requires=["setuptools_scm"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "pytest11": [
            "schema = pytest_schema",
        ],
    },
)
