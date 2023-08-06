from setuptools import setup, find_packages

with open("README.md", "r") as file:
    readme_content = file.read()

setup(
    name="deetlist",
    version="1.3",
    license="MIT License",
    author="Marcuth",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    author_email="marcuth2006@gmail.com",
    keywords="dragoncity dcutils tools",
    description=f"Fetcher/scraper of https://deetlist.com/dragoncity/",
    packages=[ "deetlist/" + x for x in find_packages("deetlist") ]
)