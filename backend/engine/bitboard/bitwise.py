def get_bit(value, n):
    return (value >> n) & 1

def set_bit(value, n):
    return value | (1 << n)

def clear_bit(value, n):
    return value & ~(1 << n)

def lshift(value, n):
    return (value << n) & 0xFFFFFFFFFFFFFFFF

def rshift(value, n):
    return (value >> n)