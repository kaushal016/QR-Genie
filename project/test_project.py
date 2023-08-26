import pytest
from project import validate_url,simple_qr,custom_qr

def test_validate_url():
    assert validate_url('https://www.google.com') == True
    assert validate_url('google.com') == False
    assert validate_url('kaushal') == False
    assert validate_url('http//google.com') == False
    assert validate_url('https://www.pll.harvard.edu') == True


def test_simple_qr():
    assert simple_qr('https://kaushal.com') == 'kaushal.png'
    assert simple_qr('https://vcacs.ac.in') != 'vcacs.ac.png'
    assert simple_qr('https://parivahan.gov.in') != 'parivahan.gov.in.png'


def test_custom_qr():
    assert custom_qr("https://oneplus.com","example_assets/one-plus-logo.png","white") == 'oneplus'
    assert custom_qr("https://parivahan.gov.in","example_assets/one-plus-logo.png","white") != 'parivahan'
    assert custom_qr("https://vcacs.ac.in","example_assets/one-plus-logo.png","white") != 'vcacs.gov.in'




