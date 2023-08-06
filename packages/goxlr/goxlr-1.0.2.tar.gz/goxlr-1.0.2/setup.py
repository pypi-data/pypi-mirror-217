from setuptools import setup, find_packages

setup(
    name="goxlr",
    version="1.0.2",
    description="A Python wrapper for the GoXLR Utility API.",
    url="https://github.com/samcarsonx/goxlr",
    author="Sam Carson",
    author_email="sam@samcarson.co.uk",
    license="None",
    packages=find_packages(),
    install_requires=["asyncio", "websockets", "json", "ctypes", "enum"],
    python_requires=">=3.6",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
