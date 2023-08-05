from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="SimuConvert",
    version="0.0.1",
    author="Yanzhong Huang",
    author_email="yanzhong.huang@outlook.com",
    description="A package for converting private fund equity data ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yanzhong-Hub/SimuConvert",
    package_dir={"": "SimuConvert"},
    packages=find_packages(where="SimuConvert"),
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    
    extras_require={
        "dev": [
            "pytest>=7.0",
            "twine>=4.0.2",]
    },
    install_requires=[
        "pandas>=1.5.0",
        "openpyxl>=3.0.0",
        ], 

)
