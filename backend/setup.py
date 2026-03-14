import os
from setuptools import setup, find_packages

def parse_requirements():
    """Reads the dependencies from requirements.txt."""
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if not os.path.exists(req_file):
        return []
        
    with open(req_file, 'r') as f:
        # Include packages, strip out inline and block comments
        return [
            line.split('#')[0].strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="mindforge-backend",
    version="0.1.0",
    description="MINDFORGE Backend API and Processing Engine",
    author="MINDFORGE Team",
    packages=find_packages(),
    install_requires=parse_requirements(),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Environment :: Web Environment",
        "Framework :: FastAPI",
        "Operating System :: OS Independent",
    ]
)
