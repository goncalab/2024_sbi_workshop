from setuptools import find_packages, setup

NAME = "sbi_workshop"
DESCRIPTION = "TODO"
URL = "TODO"
AUTHOR = "N.Krouglova, G. Moss"
REQUIRES_PYTHON = ">=3.8.0"

REQUIRED = [
    "sbi",
    "torch",
    "numpy",
    "matplotlib",
    "scikit-learn",
    "scipy",
    "cython",
    "jupyter",
]

EXTRAS = {
    "dev": [
        "autoflake",
        "black",
        "deepdiff",
        "flake8",
        "isort",
        "ipykernel",
        "jupyter",
        "pep517",
    ],
}

setup(
    name=NAME,
    version="0.1.0",
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="AGPLv3",
)
