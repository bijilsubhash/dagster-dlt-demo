from setuptools import find_packages, setup

setup(
    name="dagster_dlt_demo",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    py_modules=["main"],
    install_requires=[
        "dagster",
        "dagster-cloud",
        "paramiko>=3.3.1",
    ],
    extras_require={"dev": ["dagster-webserver"]},
)
