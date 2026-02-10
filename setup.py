from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sewing-pattern-generator",
    version="0.2.0",
    author="CaveroBen",
    description="A simple interface to OpenPattern for generating professional sewing patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CaveroBen/Sewing_Pattern_Generator",
    py_modules=["generate_patterns"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "matplotlib>=3.5.0",
    ],
)
