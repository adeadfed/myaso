#pragma once
#include <Windows.h>
#include <gdiplus.h>
#include <string>
using namespace Gdiplus;

namespace ImageSources {
	class ImageSource {
	public:
		ImageSource() {}

		virtual Bitmap* loadImage(LPCTSTR loc = L"") {
			return NULL;
		};
	};
};

