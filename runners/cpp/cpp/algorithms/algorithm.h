#pragma once
#include <gdiplus.h>
using namespace Gdiplus;

namespace Algorithms {
	class Algorithm {
	protected:
		uint8_t* payload_data;
		int payload_size;

	public:
		Algorithm() {};

		uint8_t* Read(Bitmap* bmp, int pb) {
			payload_data = new uint8_t[pb];
			payload_size = pb;
			_do_Read(bmp);
			return payload_data;
		};

		virtual void _do_Read(Bitmap* bmp) {};
	};
}
