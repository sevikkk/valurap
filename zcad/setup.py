from setuptools import find_packages, setup

setup(
    name="zcad",
    version="0.0.1",
    url="https://github.com/sevikkk/valurap.git",
    author="Vsevolod Lobko",
    author_email="seva@sevik.org",
    description="Valurap zcad model",
    packages=find_packages(),
    install_requires=["zencad"],
)
