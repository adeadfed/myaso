#include <gdiplus.h>
using namespace Gdiplus;

Gdiplus::Bitmap* load_image(LPCTSTR filename) {
    // load image
    Gdiplus::Bitmap* bmp = Gdiplus::Bitmap::FromFile(filename);
    return bmp;
}