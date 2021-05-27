#pragma once
#include <Windows.h>
#include <gdiplus.h>
#include <string>
using namespace Gdiplus;

namespace ImageSources {
	class ImageSource {
		Bitmap* bm;
	public:
		std::wstring location;

		ImageSource(LPCTSTR loc = L"") {
			location = loc;
			bm = NULL;
		}

		virtual Bitmap* loadImage() {};
	};
};

