from setuptools import find_packages, setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="hydrogibs",
    version="0.0.21",
    description="A personal hydrology and hydraulics package"
                " based on Christophe Ancey's teaching: "
                "http://fr.ancey.ch/cours/masterGC/cours-hydraulique.pdf",
    package_dir={"": "hydrogibs"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="giboul",
    author_email="axel.giboulot@epfl.ch",
    license="MIT",
    install_requires=["numpy", "scipy"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3",
)
