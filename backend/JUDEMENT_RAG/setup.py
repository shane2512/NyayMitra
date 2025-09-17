import os
from setuptools import setup, find_packages

# Get requirements from requirements.txt
with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(
    name="legal_rag",
    version="0.1.0",
    description="Legal Judgment Analysis using RAG with Gemma 2B",
    author="NyayMitra Team",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "legal_rag=demo:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Legal Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)