from setuptools import find_packages, setup

setup(
    name="dagster_dlt_demo",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dlt",
        "dagster-gcp",
        "dlt[filesystem]",
        "paramiko>=3.3.1",
        "polars>=1.32.0",
        "polars-lts-cpu>=1.32.0",
        "python-json-logger>=2.0.9",
    ],
    extras_require={"dev": ["dagster-webserver"]},
)
