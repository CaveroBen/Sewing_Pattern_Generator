from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sewing-pattern-generator",
    version="0.1.0",
    author="CaveroBen",
    description="A Python script to generate bespoke sewing patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CaveroBen/Sewing_Pattern_Generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "matplotlib>=3.5.0",
        "numpy>=1.21.0",
        "scipy>=1.8.0",
        "Pillow>=10.2.0",
        "reportlab>=3.6.13",
    ],
    entry_points={
        "console_scripts": [
            "generate-pattern=pattern_generator.cli:main",
        ],
    },
)
