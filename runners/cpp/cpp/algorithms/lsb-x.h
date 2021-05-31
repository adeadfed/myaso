#pragma once
#include "algorithm.h"

namespace Algorithms {
    class LSBX : public Algorithm {
    private:
        int channel;

        uint8_t getLsb(uint8_t target, uint8_t source) {
            return (target << 1) | (source & 1);
        }

    public:
        // redefine main constructor to include payload specific params
        LSBX(int c) : Algorithm() {
            channel = c;
        }
        
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


                    if (length <= 0) {
                        payload_data[pos / 8] = 0;
                        return;
                    }

                    payload_data[pos / 8] = getLsb(payload_data[pos / 8], channels[channel]);
                    pos++;
                    length--;
                }
            }
        }
    };
}