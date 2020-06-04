import pytest

from coords import get_device_coords


@pytest.mark.parametrize('input_data,coord', [
        [(51, 51), (50, 90)], # 1
        [(63, 45), (60, 80)], # 2
        [(76, 42), (70, 71)], # 3
    ])
def test_derive_coords(input_data, coord):
    x, y = get_device_coords(*input_data)
    assert x == coord[0]
    assert y == coord[1]
