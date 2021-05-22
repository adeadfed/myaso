#pragma once
#include <Windows.h>
#include <gdiplus.h>
#include <string>
using namespace Gdiplus;

namespace Reader {
	class Delivery {
	public:
		std::wstring location;
		Bitmap* bm;

		Delivery(LPCTSTR loc) {
			location = loc;
			bm = NULL;
		}

		Delivery() {};

		virtual void loadImage() {};
	};
};

