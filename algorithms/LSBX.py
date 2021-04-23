from bitarray import bitarray
from PIL import Image

def set_lsb(byte, value):
    """
    set last bit to 1 by doing bitwise OR with 0b00000001
    set last bit to 0 by doing bitwise AND with 0b11111110
    """
    return byte | 0b1 if value else byte & ~0b1


# get last bit value by doing bitwise AND with 0b00000001
def get_lsb(byte):
    return byte & 0b1

def embed_data(img: Image, channel: str, payload: bitarray):
    
    channels = {'r':0, 'g':0, 'b':0}
    
    # maximum number of less significant bits
    max_len = img.height * img.width * 3

    if len(payload) > max_len:
        print('[-] Too much to handle!')
        return

    # iterate over pixels left to right, top to bottom
    for y in range(img.height):
        for x in range(img.width):
            # get initial values
            channels['r'], channels['g'], channels['b'] = img.getpixel((x,y))
            
            # print(r,g,b)
            # set lsb of each color to target value
            # pop first shellcode bit and set it in the color 

            # FYI, in binary, (r,g,b) is stored in reverse (b,g,r)
            # https://stackoverflow.com/questions/9296059/read-pixel-value-in-bmp-file/38440684
            if payload: channels[channel] = set_lsb(channels[channel], payload.pop(0))
            
            img.putpixel((x,y), (channels['r'], channels['g'], channels['b']))


def extract_data(img: Image, channel: str, max_bits: int) -> bitarray:
    payload = bitarray()
   
    channels = {'r':0, 'g':0, 'b':0}

    # Iterate over pixels left to right, top to bottom
    for y in range(img.height):
        for x in range(img.width):
            # get initial values
            channels['r'], channels['g'], channels['b'] = img.getpixel((x,y))
            
            if max_bits > 0:
                lsb_bit = get_lsb(channels[channel])
                payload.append(lsb_bit)

                max_bits -= 3
            else:
                return payload
