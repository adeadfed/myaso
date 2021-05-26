#pragma once
#include "algorithm.h"

namespace Reader {
    class LSBX : public Algorithm {
    private:
        int channel;

        char getLsb(char target, char source) {
            return (target << 1) | (source & 1);
        }

    public:
        // inherit default constructor from parent
        LSBX() : Algorithm() {}
        // redefine main constructor to include payload specific params
        LSBX(Bitmap* bm, int pb, int c) : Algorithm(bm, pb) {
            channel = c;
        }

        void readImage() {
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