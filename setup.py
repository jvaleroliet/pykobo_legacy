from setuptools import setup, find_packages

setup(
    name="pykobo_legacy",
    version="0.1",
    author="Juan Valero",
    packages=find_packages(),
    install_requires=[
        "inquirer==3.1.3",
        "numpy==1.23.5",
        "openpyxl==3.0.10",
        "pandas==1.5.3",
        "Pillow==9.4.0",
       " Requests==2.28.2",
        "utils==1.0.1"
        ],
    include_package_data=True,
)
