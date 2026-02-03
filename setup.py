from setuptools import setup, find_packages

setup(
    name="Topsis-Pooja-102303845",
    version="1.0.1",
    author="Pooja",
    description="TOPSIS implementation using Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pandas", "numpy"],
    entry_points={
        "console_scripts": [
            "topsis=topsis_pooja_102303845.topsis:main"
        ]
    },
)
