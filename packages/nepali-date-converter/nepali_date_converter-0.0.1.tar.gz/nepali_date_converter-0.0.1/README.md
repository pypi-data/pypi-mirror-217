# Nepali Date Converter

This is a simple project that converts dates between nepali and english dates.


## Installation
Run the following command to install:

'''python
pip install nepali_date_converter
'''

## Usage

'''python

# Generate "2080-03-18"
from nepali_date_converter import english_to_nepali_converter
english_to_nepali_converter(2023,7,3)

# Generate "2023-07-03"
from nepali_date_converter import nepali_to_english_converter
nepali_to_english_converter(2080, 3, 18)
'''

# Developing nepali_date_converter

To install nepali_date_converter, along with the tools you need to develop and run tests, run the following in your virtualenv:

'''bash
$ pip install -e .[dev]
'''