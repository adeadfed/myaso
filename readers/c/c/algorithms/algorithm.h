#pragma once
#include <gdiplus.h>
using namespace Gdiplus;

namespace Algorithms {
	class Algorithm {
		uint8_t* payload_data;
		int payload_bits;

	public:
		Algorithm() {};

		uint8_t* readImage(Bitmap* bmp, int payload_bits) {
			payload_data = new uint8_t[payload_bits / 8];
			payload_bits = payload_bits;
			_do_readImage(bmp);
			return payload_data;
		};

		virtual void _do_readImage(Bitmap* bmp) {};
	};
}
