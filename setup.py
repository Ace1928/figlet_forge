#!/usr/bin/env python3
"""
Figlet Forge setup.py file.
For compatibility with older tools, use this instead of pyproject.toml.
For modern usage, prefer pyproject.toml.
"""

from setuptools import find_packages, setup

from src.figlet_forge.version import (
    __author__,
    __author_email__,
    __description__,
    __version__,
)

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="figlet_forge",
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ace1928/figlet_forge",
    project_urls={
        "Documentation": "https://figlet-forge.readthedocs.io/",
        "Source": "https://github.com/Ace1928/figlet_forge",
        "Tracker": "https://github.com/Ace1928/figlet_forge/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Fonts",
        "Topic :: Artistic Software",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "colorama>=0.4.3; sys_platform == 'win32'",
        "importlib-resources>=1.4.0; python_version < '3.9'",
        "typing-extensions>=4.0.0; python_version < '3.8'",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
            "tox>=4.0.0",
            "twine>=4.0.0",
            "build>=1.0.0",
            "termcolor>=2.0.0",
            "pyfiglet>=0.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "figlet_forge=figlet_forge.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
