import os
from setuptools import setup

dir_path = os.path.dirname(os.path.realpath(__file__))


def readme() -> str:
    with open("README.md", encoding='utf-8') as file:
        file_data = file.read()
    return file_data


setup(
    name="cloudflared",
    version="1.0.0.1",
    description="A Python package to interact with cloudflared",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/SigireddyBalaSai/cloudflared.py",
    author="Sigireddy BalaSai",
    author_email="sigireddybalasai@gmail.com",
    license="Apache-2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["cloudflared"],
    include_package_data=True,
    install_requires=["setuptools_scm"],
)
