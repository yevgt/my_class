import pytest
from simple_math import SimpleMath

class SimpleMath:
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

math = SimpleMath()

@pytest.fixture
def math():
    return SimpleMath()

def test_square_positive(math):
    assert math.square(2) == 4

def test_square_negative(math):
    assert math.square(-3) == 9

def test_square_zero(math):
    assert math.square(0) == 0

def test_cube_positive(math):
    assert math.cube(3) == 27

def test_cube_negative(math):
    assert math.cube(-3) == -27

def test_cube_zero(math):
    assert math.cube(0) == 0

def test_divide_by_zero(math):
    with pytest.raises(ZeroDivisionError):
        math.divide(1, 0)
