from setuptools import setup, find_packages

setup(
    name="growth-tracker-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer==0.12.3",
        "pyyaml==6.0.1",
        "requests==2.31.0",
        "tabulate==0.9.0",
        "python-dateutil==2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "growth-tracker=growth_tracker.cli:app",
        ],
    },
)