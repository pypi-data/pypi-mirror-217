import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name                = 'f_yolov8',
    version             = '0.0.3',
    author              = 'jskim1102',
    author_email        = 'deepi.contact.us@gmail.com',
    long_description=long_description,
    install_requires    =  requirements,
    packages=setuptools.find_packages(),
    python_requires     = '>=3.8',
)