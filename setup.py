from setuptools import find_packages, setup

setup(
    name="dagster_dlt_demo",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dlt",
        "paramiko>=3.3.1",
        "python-json-logger>=2.0.9",
    ],
    extras_require={"dev": ["dagster-webserver"]},
)
