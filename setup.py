from setuptools import setup

setup(
    name="pi-visit",
    version="0.1.0",
    packages=["pi_visit"],
    entry_points={
        "console_scripts": [
            "pi_visit = pi_visit.__main__:main"
        ]
    },
)
