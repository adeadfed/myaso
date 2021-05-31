#pragma once
#include "algorithm.h"

namespace Algorithms {
    class LSB : public Algorithm {
    private:
        uint8_t GetLSB(uint8_t target, uint8_t source) {
            return (target << 1) | (source & 1);
        }
    public:
        // inherit constructors from parent
        LSB() : Algorithm() {};

        void _do_Read(Bitmap* bmp) {
            Color c;
            uint8_t channels[3];

            int bit_length = payload_size * 8;
            int pos = 0;

            for (int i = 0; i < bmp->GetHeight(); i++) {
                for (int j = 0; j < bmp->GetWidth(); j++) {

                    bmp->GetPixel(j, i, &c);

                    channels[0] = c.GetR();
                    channels[1] = c.GetG();
                    channels[2] = c.GetB();

                    for (int k = 0; k < 3; k++) {
                        if (bit_length <= 0) {
                            payload_data[pos / 8] = 0;
                            return;
                        }

                        payload_data[pos / 8] = GetLSB(payload_data[pos / 8], channels[k]);
                        pos++;
                        bit_length--;
                    }
                }
            }
        };
    };
}

