from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name="stocks-cli",
    version="0.1.1",
    author="GBCS",
    author_email="gbcs@embl.de",
    packages=["cli", "stocks", "stocks.assaysniffer", "stocksapi"],
    data_files=[('cli', ['cli/stockscli.ini'])],
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        "dev": ["setuptools==67.7.2"]
    },
    entry_points={
        "console_scripts": [
            "stocks-cli = cli.__main__:main",
        ],
    },
    url="https://www.embl.org/research/units/genome-biology/genome-biology-computational-support/",
    description="Command Line Interface to the STOCKS server"
)
