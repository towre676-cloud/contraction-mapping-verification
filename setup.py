
from setuptools import setup, find_packages

setup(
    name="contraction-mapping-verification",
    version="0.1.0",
    description="Verification framework for contraction mappings with interval and spectral helpers",
    author="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["numpy", "scipy"],
    entry_points={"console_scripts": ["verify-gaps=verify_gaps:main"]},
    python_requires=">=3.9",
)
