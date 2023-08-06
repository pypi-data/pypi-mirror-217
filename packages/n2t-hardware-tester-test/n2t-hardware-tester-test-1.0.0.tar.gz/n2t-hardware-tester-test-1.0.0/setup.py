from setuptools import find_packages, setup

setup(
    name="n2t-hardware-tester-test",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "PyYAML~=6.0",
        "requests",
        "typer",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
    ],
    entry_points={
        "console_scripts": [
            "n2t-test=n2t_hardware_tester.main:app",
        ],
    },
)
