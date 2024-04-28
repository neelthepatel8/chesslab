from engine.bitmanipulation.bitwise import get_bit, set_bit, clear_bit

def test_get_bit():
    assert get_bit(0b0101, 0) == True  
    assert get_bit(0b0101, 1) == False 
    assert get_bit(0b0101, 2) == True 
    assert get_bit(0b0101, 3) == False 

def test_set_bit():
    assert set_bit(0b0101, 1) == 0b0111  
    assert set_bit(0b0101, 0) == 0b0101 
    assert set_bit(0b0101, 3) == 0b1101 

def test_clear_bit():
    assert clear_bit(0b0101, 0) == 0b0100  
    assert clear_bit(0b0101, 2) == 0b0001 
    assert clear_bit(0b0101, 3) == 0b0101