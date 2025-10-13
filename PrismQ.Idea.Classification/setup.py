"""Setup configuration for PrismQ.Idea.Classification package."""

from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prismq-idea-classification",
    version="1.0.0",
    author="PrismQ Team",
    author_email="dev@prismq.io",
    description="Platform-agnostic content classification for PrismQ Idea Sources ecosystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nomoos/PrismQ.Idea.Classification",
    packages=find_namespace_packages(include=['prismq.*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - 100% stdlib
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
        "test": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    keywords="prismq classification content-analysis story-detection nlp",
    project_urls={
        "Bug Reports": "https://github.com/Nomoos/PrismQ.Idea.Classification/issues",
        "Source": "https://github.com/Nomoos/PrismQ.Idea.Classification",
        "Documentation": "https://github.com/Nomoos/PrismQ.Idea.Classification/docs",
    },
)
