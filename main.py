# C implementation reads pixels left to right, top to bottom
# Python implementation reads pixels left to right, bottom to top!



from PIL import Image

# get bits from byte in MSB format and normalize them to 8 bits per byte
def get_bits(n):
    for x in range(0,8):
        yield (n & (0b10000000 >> x))


# force set last bit to 1 by doing bitwise OR with 0b00000001 
# force set last bit to 0 by doing bitwise AND with 0b11111110
def set_lsb(byte, value):
    return byte | 1 if value else byte & ~1


# get last bit value by doing bitwise AND with 0b00000001
def get_lsb(byte):
    return byte & 1


def read_sc_file(sc_filename):
    with open(sc_filename, 'rb') as f:
       bytes = f.read()
    
    bits = list()
    
    for byte in bytes:
        for x in get_bits(byte):
            # normalize bitwise and result to 1 or 0
            bits.append(int(bool(x)))
    

    # TODO: should probably change this
    # append 64 trailing zeros to set the payload end
    for _ in range(0, 64):
        bits.append(0)

    return bits



def save_encoded_image(img_filename, shellcode):
    img = Image.open(img_filename)

    
    # Iterate over pixels left to right, top to bottom
    for y in reversed(range(img.height)):
        for x in range(img.width):
            # get initial values
            r, g, b = img.getpixel((x,y))
            
            # set lsb of each color to target value
            # pop first shellcode bit and set it in the color 
            if (len(shellcode)):
                r = set_lsb(r, shellcode.pop(0))
                g = set_lsb(g, shellcode.pop(0))
                b = set_lsb(b, shellcode.pop(0))
            
            img.putpixel((x,y), (r, g, b))
    img.save('helpme.bmp')


def read_encoded_image(img_filename):
    img = Image.open(img_filename)
    
    message_bits = list()
    
    zero_counter = 0
    
    # Iterate over pixels left to right, top to bottom
    for y in reversed(range(img.height)):
        for x in range(img.width):
            # get initial values
            r, g, b = img.getpixel((x,y))
            print(r, g, b)
            
            # TODO: should probably change this
            if (zero_counter < 32):
                r_bit = get_lsb(r)
                g_bit = get_lsb(g)
                b_bit = get_lsb(b)

                if not r_bit: zero_counter += 1
                if not g_bit: zero_counter += 1
                if not b_bit: zero_counter += 1

                if r_bit or g_bit or b_bit:
                    zero_counter = 0

                message_bits.append(r_bit)
                message_bits.append(g_bit)
                message_bits.append(b_bit)
            else:
                print(message_bits)
                return 0


# shellcode = read_sc_file('test.txt')
# print(shellcode)
# save_encoded_image('cat.bmp', shellcode)
read_encoded_image('Untitled.bmp')

