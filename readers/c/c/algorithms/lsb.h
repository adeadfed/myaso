#include <gdiplus.h>
using namespace Gdiplus;

char get_lsb(char target, char source) {
    return (target << 1) | (source & 1);
}

void read_image(Gdiplus::Bitmap* bmp, char * payload_data, int payload_bits) {
    Color c;
    char channels[3];

    int length = payload_bits;
    int pos = 0;

    for (int i = 0; i < bmp->GetHeight(); i++) {
        for (int j = 0; j < bmp->GetWidth(); j++) {

            bmp->GetPixel(j, i, &c);

            channels[0] = c.GetR();
            channels[1] = c.GetG();
            channels[2] = c.GetB();

            for (int k = 0; k < 3; k++) {
                if (length <= 0) {
                    payload_data[pos / 8] = 0;
                    return;
                }

                payload_data[pos / 8] = get_lsb(payload_data[pos / 8], channels[k]);
                pos++;
                length--;
            }
        }
    }
}