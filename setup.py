from setuptools import setup

setup(
    name="signin-pi",
    version="0.1.0",
    packages=["signin_pi"],
    entry_points={
        "console_scripts": [
            "signin_pi = signin_pi.__main__:main"
        ]
    },
)
