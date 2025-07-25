from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Hotel Reservation Prediction_DS-Project",
    version="0.1",
    author="Rhitwik Prakash",
    packages=find_packages(),
    install_requires = requirements,
    description="An End-to-End Data Science project to predict hotel reservation cancellations using machine learning",
)