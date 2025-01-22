from setuptools import find_packages, setup

setup(
    name="hitdexter",
    version="0.3.1",
    maintainer="Johannes Kirchmair",
    maintainer_email="johannes.kirchmair@univie.ac.at",
    packages=find_packages(),
    url="https://github.com/molinfo-vienna/hitdexter",
    long_description=open("README.md").read(),
    include_package_data=True,
    install_requires=[
        "rdkit==2020.09.1",
        "scikit_learn==0.23.2",
        "numpy==1.19.2",
        "nerdd-module>=0.3.6",
        "fpsim2==0.2.8",
        "chembl_structure_pipeline==1.0.0",
        # install importlib-resources and importlib-metadata for old Python versions
        "importlib-resources>=5; python_version<'3.9'",
        "importlib-metadata>=4.6; python_version<'3.10'",
    ],
    extras_require={
        "dev": [
            "mypy",
            "ruff",
        ],
        "test": [
            "pytest",
            "pytest-watch",
            "pytest-cov",
            "pytest-bdd==7.3.0",
            "hypothesis",
            "hypothesis-rdkit",
        ],
    },
    entry_points={
        "console_scripts": [
            "hitdexter3=hitdexter.__main__:main",
        ],
    },
)
