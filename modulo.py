def test_all_positive():
    a = 22
    b = 10
    q = a//b
    r = a%b
    assert a == b*q + r
    assert 0 <= r < abs(b)


def test_all_negative():
    a = -22
    b = -10
    q = a//b
    r = a%b
    assert a == b*q + r
    assert 0 <= r < abs(b)


def test_dividend_negative():
    a = -22
    b = 10
    q = a//b
    r = a%b
    assert a == b*q + r
    assert 0 <= r < abs(b)


def test_divisor_negative():
    a = 22
    b = -10
    q = a//b
    r = a%b
    assert a == b*q + r
    assert 0 <= r < abs(b)


# fmod instead %
import math

def test_all_positive_fmod():
    a = 22
    b = 10
    q = a//b
    r = math.fmod(a, b)
    assert a == b*q + r
    assert 0 <= r < abs(b)


def test_all_negative_fmod():
    a = -22
    b = -10
    q = a//b
    r = math.fmod(a, b)
    assert a == b*q + r
    assert 0 <= r < abs(b)


def test_dividend_negative_fmod():
    a = -22
    b = 10
    q = a//b
    r = math.fmod(a, b)
    assert a == b*q + r
    assert 0 <= r < abs(b)


def test_divisor_negative_fmod():
    a = 22
    b = -10
    q = a//b
    r = math.fmod(a, b)
    assert a == b*q + r
    assert 0 <= r < abs(b)
