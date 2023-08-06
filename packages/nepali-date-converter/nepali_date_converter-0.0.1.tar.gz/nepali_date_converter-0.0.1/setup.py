from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'NepaliDateConverter'

with open("README.md","r") as fh:
    long_description = fh.read() 
# Setting up
setup(
    name="nepali_date_converter",
    version=VERSION,
    author="Gopal kisi",
    author_email="gkisi2772@gmail.com",
    url= "https://github.com/GKisi27/nepali_date_converter",
    description=DESCRIPTION,
    py_modules= ["nepali_date_converter"],
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["nepali_datetime"],
    keywords=['python', 'tutorial', 'date_converter', 'bikram sambat', 'nepali date converter', 
              'nepali datetime', 'bs to ad converter', 'ad to bs converter', 'nepali datetime'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_dir={"":"src"},
    extras_require={
        "dev":[
        "pytest >= 7.4",
        "twine"
        ],
    },
)