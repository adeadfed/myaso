#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <fstream>
#include <bitset>


char get_lsb(char target, char source) {
    return (target << 1) | (source & 1);
}


void ReadBMP(std::string filename)
{
    char header[54];
    int height, width;

    std::ifstream file(filename);
  
    file.read(header, 54);


    /*
    * Get image width and height in pixels
    * 
    * Beware, some BMP images store negative values within the header fields.
    * This means that the coordinates of BMP image is flipped
    */

    width = abs(*(int *)(header + 18));
    height = abs(*(int *)(header + 22));


   /*
   * Get pixel row length in bytes
   * 
   * BMP requires padding to be a multiple of 4 bytes.
   * Colors themselves are stored as 3 bytes. 
   * We must round length to next nearest multiple of 4 
   * https://en.wikipedia.org/wiki/BMP_file_format#Pixel_storage
   */

    int row_length = 4 * ((width + 1) * 3 / 4);
    
    char* payload_data;
    
    int bits_to_read = 360;
    int bits_read = 0;

    char* row_data = new char[row_length];
    char r, g, b;

    char temp = 0;

    for (int i = 0; i < height; i++)
    {
        file.read(row_data, row_length);
        for (int j = 0; j < width * 3; j += 3)
        {
            if (bits_to_read) {
                /*
                * In binary, pixels are actually stored in reversed format (B, G, R)
                * https://stackoverflow.com/questions/9296059/read-pixel-value-in-bmp-file/38440684
                */


                b = row_data[j];
                g = row_data[j + 1];
                r = row_data[j + 2];
                
                temp = get_lsb(temp, r);
                temp = get_lsb(temp, g);
                temp = get_lsb(temp, b);

                bits_to_read -= 3;
            }
            else {
                file.close();
                return;
            }
        }
    }
}


int main() {
    ReadBMP("C:\\Users\\Blackberry\\Desktop\\projects\\yet-another-shellcode-obfuscator\\helpme.bmp");
    // ReadBMP("C:\\Users\\Blackberry\\Desktop\\Untitled.bmp");
    // ReadBMP("output-onlinerandomtools2.bmp");
    return 0;
}