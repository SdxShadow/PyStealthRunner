
from setuptools import setup, find_packages
try:
    from wheel.bdist_wheel import bdist_wheel
    cmdclass = {'bdist_wheel': bdist_wheel}
except ImportError:
    cmdclass = {}

setup(
    name="pystealthrunner",
    version="1.0.0",
    description="Run Python scripts as background processes for ethical hacking and automation.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="SdxShadow",
    author_email="team.sdxshadow@gmail.com",
    url="https://github.com/SdxShadow/PyStealthRunner",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[

    ],
    extras_require={
        "dev": [
            "pytest",
            "build",
            "twine",
            "wheel"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    include_package_data=True,
    # No entry_points needed for this package
    cmdclass=cmdclass
)