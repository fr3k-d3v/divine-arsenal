import pytest
from divine.traditions import SIZE,planetary_kamea,magic_square,verify_magic

@pytest.mark.parametrize("planet",list(SIZE))
def test_all_seven_magic_squares(planet):
    data=planetary_kamea(planet)
    assert data["validated"] is True
    assert verify_magic(data["grid"])
    assert data["constant"]==data["order"]*(data["order"]**2+1)//2

@pytest.mark.parametrize("n",[3,4,5,6,7,8,9,10,11,12])
def test_square_algorithm_across_orders(n):
    assert verify_magic(magic_square(n))

def test_invalid_planet_fails_closed():
    with pytest.raises(ValueError):
        planetary_kamea("Pluto")
