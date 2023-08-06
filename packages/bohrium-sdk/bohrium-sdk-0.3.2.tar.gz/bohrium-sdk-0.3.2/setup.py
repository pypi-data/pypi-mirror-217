from setuptools import setup
import setuptools
setup(
    name="bohrium-sdk",
    version="0.3.2",
    author="dingzhaohan",
    author_email="dingzh@dp.tech",
    url="https://github.com/dingzhoahan",
    description="bohrium openapi python sdk",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyhumps==3.8.0",
        "rich"
    ],
    python_requires='>=3.7',
    entry_points={}
)

