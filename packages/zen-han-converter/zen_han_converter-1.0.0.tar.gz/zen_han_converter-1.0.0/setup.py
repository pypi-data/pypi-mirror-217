from setuptools import setup, find_packages


setup(
    name="zen_han_converter",
    version="1.0.0",
    author="n4cl",
    author_email="devn4cl@gmail.com",
    description="Converts full-width and half-width characters.",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/n4cl/zen_han_converter.git",
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11"
    ]
)
