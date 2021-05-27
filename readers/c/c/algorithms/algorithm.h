#pragma once
#include <gdiplus.h>
using namespace Gdiplus;

namespace Algorithms {
	class Algorithm {
	public:
		uint8_t* payload_data;
		int payload_bits;

		Algorithm(int pb) {
			payload_bits = pb;

			payload_data = new uint8_t[payload_bits / 8];
		}

		Algorithm() {};

		virtual void readImage(Bitmap * bmp, int payload_bits) {};
	};
}
