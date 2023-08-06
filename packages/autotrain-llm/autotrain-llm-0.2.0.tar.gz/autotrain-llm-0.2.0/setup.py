# Lint as: python3
# pylint: enable=line-too-long

from setuptools import find_packages, setup


with open("README.md") as f:
    long_description = f.read()

# fetch requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

INSTALL_REQUIRES = [i.strip() for i in requirements]

QUALITY_REQUIRE = [
    "black",
    "isort",
    "flake8",
]

EXTRAS_REQUIRE = {
    "dev": INSTALL_REQUIRES + QUALITY_REQUIRE,
    "quality": INSTALL_REQUIRES + QUALITY_REQUIRE,
}

if __name__ == "__main__":
    setup(
        name="autotrain-llm",
        description="autotrain_llm",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Abhishek Thakur",
        url="https://github.com/huggingface/autotrain-llm",
        license="Apache License",
        packages=find_packages(),
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        entry_points={"console_scripts": ["autotrain-llm=autotrain_llm.cli.cli:main"]},
        platforms=["linux", "unix"],
        python_requires=">=3.9",
        classifiers=[
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.8",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
        ],
    )
