# C implementation reads pixels left to right, top to bottom
# Python implementation reads pixels left to right, bottom to top!


# TODO: rewrite bit operations on python bitarray


from PIL import Image
from bitarray import bitarray
from bitarray.util import int2ba, ba2int




# force set last bit to 1 by doing bitwise OR with 0b00000001 
# force set last bit to 0 by doing bitwise AND with 0b11111110
def set_lsb(byte, value):
    return byte | 0b1 if value else byte & ~0b1


# get last bit value by doing bitwise AND with 0b00000001
def get_lsb(byte):
    return byte & 0b1


def read_sc_file(sc_filename):
    with open(sc_filename, 'rb') as f:
        sc_bits = bitarray()
        sc_bits.fromfile(f)
    
    return sc_bits.tolist()


def save_encoded_image(src_img_filename, tgt_img_filename, sc_bits):
    img = Image.open(src_img_filename)

    # maximum number of less significant bits
    max_len = img.height * img.width * 3

    if len(sc_bits) > max_len:
        print('[-] Too much to handle!')
        return

    # iterate over pixels left to right, top to bottom
    for y in reversed(range(img.height)):
        for x in range(img.width):
            # get initial values
            r, g, b = img.getpixel((x,y))
            
            # print(r,g,b)
            # set lsb of each color to target value
            # pop first shellcode bit and set it in the color 

            # in binary, (r,g,b) is stored in reverse (b,g,r)
            # https://stackoverflow.com/questions/9296059/read-pixel-value-in-bmp-file/38440684
            if (sc_bits): b = set_lsb(b, sc_bits.pop(0))
            if (sc_bits): g = set_lsb(g, sc_bits.pop(0))
            if (sc_bits): r = set_lsb(r, sc_bits.pop(0))
            
            
            img.putpixel((x,y), (r, g, b))
    img.save(tgt_img_filename)


def read_encoded_image(img_filename, length):
    img = Image.open(img_filename)
    
    message_bits = bitarray()
   
    # Iterate over pixels left to right, top to bottom
    for y in reversed(range(img.height)):
        for x in range(img.width):
            # get initial values
            r, g, b = img.getpixel((x,y))
            
            if length > 0:
                r_bit = get_lsb(r)
                g_bit = get_lsb(g)
                b_bit = get_lsb(b)

                message_bits.append(b_bit)
                message_bits.append(g_bit)
                message_bits.append(r_bit)

                length -= 3
            else:
                return message_bits.tobytes()







shellcode = read_sc_file('samples/test_small.txt')

length = len(shellcode) 
print(length)

save_encoded_image('samples/Untitled2.bmp', 'samples/howareyou.bmp', shellcode)
message = read_encoded_image('samples/howareyou.bmp', length)

print(message)
