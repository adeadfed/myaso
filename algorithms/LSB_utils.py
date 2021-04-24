def __set_lsb(byte, value):
    """
    set last bit to 1 by doing bitwise OR with 0b00000001
    set last bit to 0 by doing bitwise AND with 0b11111110
    """
    return byte | 0b1 if value else byte & ~0b1


def __get_lsb(byte):
    """get last bit by doing bitwise AND with 0b00000001"""
    return byte & 0b1

