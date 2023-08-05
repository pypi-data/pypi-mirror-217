from setuptools import setup, find_packages, Extension
import embedded_tools

description = open("README.md").read()
# Change links to stable documentation
description = description.replace("/latest/", "/stable/")

setup(
    name="embedded_tools",
    url="https://github.com/gabrielfrasantos/embedded-tools",
    version=embedded_tools.__version__,
    packages=find_packages(exclude=['docs', 'examples']),
    author="Gabriel Santos",
    description="Tools to be used on a embedded environment",
    keywords="Segger Jlink STLink RTT Serial Embedded",
    long_description=description,
    long_description_content_type='text/x-rst',
    license="MIT",
    platforms=["any"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering"
    ],
    install_requires=[
        "pytest >= 6.2.5",
        "cantools == 36.2.0",
        "intelhex == 2.3.0",
        "pyserial == 3.5",
        "pyusb == 1.2.1",
        "pyyaml == 6.0",
        "robotframework == 5.0",
    ],
    include_package_data=True,

    # Tests can be run using `python setup.py test`
    test_suite="nose.collector",
    tests_require=["nose"]
)