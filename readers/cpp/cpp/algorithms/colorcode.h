#pragma once
#include "algorithm.h"

namespace Algorithms {
    class Colorcode : public Algorithm {
    private:
        uint8_t getColorcode(uint8_t target, uint8_t source) {
            return (target << 1) | (source > (uint8_t)128);
        }
    public:
        Colorcode() : Algorithm() {}

        void _do_readImage(Bitmap* bmp) {
            Color c;
            uint8_t channels[3];

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

                        payload_data[pos / 8] = getColorcode(payload_data[pos / 8], channels[k]);
                        pos++;
                        length--;
                    }
                }
            }
        }
    };
}