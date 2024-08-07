from setuptools import setup, find_packages
import json

with open("metadata.json", encoding="utf-8") as fp:
    metadata = json.load(fp)

setup(
    name='lexibank_northernperu',
    py_modules=['lexibank_northernperu'],
    include_package_data=True,
    url=metadata.get("url", ""),
    packages=find_packages(where="."),
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'northernperu=lexibank_northernperu:Dataset',
        ]
    },
    install_requires=[
        "pylexibank>=3.0.0",
        "cldfbench==1.13.0",
        "pycldf==1.34.0",
        "csvw==3.1.3",
        "pyconcepticon==3.0.0",
    ],
    extras_require={
        'test': ['pytest-cldf']
        }
)
