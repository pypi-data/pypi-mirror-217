from setuptools import setup

setup(
    name="git_dl",
    version="1.0.0",
    description="A simple CLI app to dowload a folder from github",
    author="the-runtime",
    py_modules=["git_dl"],
    entry_points={
        "console_scripts": [
            "git_dl = git_dl.cli:cli"
        ]
    },
)
