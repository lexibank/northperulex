from setuptools import setup
import json

with open("metadata.json", encoding="utf-8") as fp:
    metadata = json.load(fp)

setup(
    name='lexibank_blumyanomamic',
    py_modules=['lexibank_blumyanomamic'],
    include_package_data=True,
    url=metadata.get("url", ""),
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'blumyanomamic=lexibank_blumyanomamic:Dataset',
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
