#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : 梁泽华Calia
# @Date : 2023/7/6 19:24
# @Description :
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="caliatestpy",
    version="0.0.1",
    author="Calia",
    author_email="cnboycalia@gmail.com",
    description="No description.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[''],
    extras_require={ },
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)