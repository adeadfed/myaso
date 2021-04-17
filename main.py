# C implementation reads pixels left to right, top to bottom
# Python implementation reads pixels left to right, bottom to top!


# TODO: rewrite bit operations on python bitarray


from PIL import Image
from bitarray import bitarray
from bitarray.util import int2ba, ba2int


# DEPRECATED

# get bits from byte in MSB format and normalize them to 8 bits per byte
# def get_8_bits(n):
#     for x in range(0,8):
#         yield (n & (0b10000000 >> x))

# # get bits from int32 in MSB format and normalize them to 32 bits
# def get_32_bits(n):
#     for x in range(0,32):
#         yield (n & (0x80000000 >> x))







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
    
    
    _, sc_len, _, _, _ = sc_bits.buffer_info()

    # get the size of shellcode payload in bits
    sc_len_bits = int2ba(sc_len, 32)

    # write the size of payload at the start
    # write the actual payload
    payload = sc_len_bits + sc_bits

    # DEPRECATED
    # bits = list()
    # for x in get_32_bits(len(bytes)):
    #      # normalize bitwise and result to 1 or 0
    #     bits.append(int(bool(x)))
    
    
    # for byte in bytes:
    #     for x in get_8_bits(byte):
    #         # normalize bitwise and result to 1 or 0
    #         bits.append(int(bool(x)))

    return payload.tolist()



def save_encoded_image(img_filename, sc_bits):
    img = Image.open(img_filename)

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
            
            # set lsb of each color to target value
            # pop first shellcode bit and set it in the color 
            if (sc_bits): r = set_lsb(r, sc_bits.pop(0))
            if (sc_bits): g = set_lsb(g, sc_bits.pop(0))
            if (sc_bits): b = set_lsb(b, sc_bits.pop(0))
            
            img.putpixel((x,y), (r, g, b))
    img.save('helpme.bmp')


def read_encoded_image(img_filename):
    img = Image.open(img_filename)
    
    message_bits = bitarray()
    # read 12 pixels
    bits_to_read = 36 
    pixel_num = 0
    
    # Iterate over pixels left to right, top to bottom
    for y in reversed(range(img.height)):
        for x in range(img.width):
            # get initial values
            r, g, b = img.getpixel((x,y))
            # print(r, g, b)
            
            if (bits_to_read > 0):
                r_bit = get_lsb(r)
                g_bit = get_lsb(g)
                # first 10 pixels (r,g,b) and 11th (r,g) 
                # contain info about message length
                
                if pixel_num == 11:
                    # calc size of actual payload
                    # drop first 32 bits
                    bits_to_read = ba2int(message_bits[:32]) * 8
                    message_bits = message_bits[32:]             

                b_bit = get_lsb(b)


                message_bits.append(r_bit)
                message_bits.append(g_bit)
                message_bits.append(b_bit)

                bits_to_read -= 3
                pixel_num += 1
            else:
                # pop extra bits if present
                while len(message_bits) % 8:
                    message_bits.pop()
                
                return message_bits.tobytes()


shellcode = read_sc_file('test_small.txt')
save_encoded_image('Untitled2.bmp', shellcode)
message = read_encoded_image('helpme.bmp')

print(message.decode('utf-8'))