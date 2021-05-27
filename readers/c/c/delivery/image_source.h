#pragma once
#include <Windows.h>
#include <gdiplus.h>
#include <string>
using namespace Gdiplus;

namespace ImageSources {
	class ImageSource {
	public:
		std::wstring location;
		Bitmap* bm;

		ImageSource(LPCTSTR loc) {
			location = loc;
			bm = NULL;
		}

		ImageSource() {};

		virtual void loadImage() {};
	};
};

