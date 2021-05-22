#pragma once
#include <gdiplus.h>
using namespace Gdiplus;

namespace Reader {
	class Algorithm {
	public:
		char* payload_data;
		int payload_bits;
		Bitmap* bmp;

		Algorithm(Bitmap* bm, int pb) {
			bmp = bm;
			payload_bits = pb;

			payload_data = new char[payload_bits / 8];
		}

		Algorithm() {};

		virtual void readImage() {};
	};
}
