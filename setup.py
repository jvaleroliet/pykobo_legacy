from setuptools import setup, find_packages

setup(
    name="pykobo_legacy",
    version="0.1",
    author="Juan Valero",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.25.2,<1.26.0",
        "pandas>=1.5.3,<2.2.0",
        # "PyDase @ git+ssh://git@github.com/ACHESP/PyDase.git@dev",
        "openpyxl==3.0.10"
        ],
    include_package_data=True,
)
