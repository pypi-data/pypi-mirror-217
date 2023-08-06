from nepali_date_converter import *

def test_english_to_nepali_converter():
    assert english_to_nepali_converter(2023,7,3) == "2080-03-18"

def test_nepali_to_english_converter():
    assert nepali_to_english_converter(2080, 3, 18) == "2023-07-03"
