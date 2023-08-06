from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name="sreddit",
    version='1.0.3',
    author="Mandy-cyber",
    author_email="",
    description='Web scraper for subreddits',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages(),
    url="https://github.com/Mandy-cyber/sreddit",
    install_requires=['selenium', 'get_chrome_driver'],
    keywords=['python', 'selenium', 'reddit', 'subreddit'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires = ">=3.6"
)