#pragma once
#include <gdiplus.h>
using namespace Gdiplus;

namespace Algorithms {
	class Algorithm {
	protected:
		uint8_t* payload_data;
		int payload_bits;

	public:
		Algorithm() {};

		uint8_t* readImage(Bitmap* bmp, int pb) {
			payload_data = new uint8_t[pb / 8];
			payload_bits = pb;
			_do_readImage(bmp);
			return payload_data;
		};

		virtual void _do_readImage(Bitmap* bmp) {};
	};
}
