#pragma once
#include <windows.h>
#include <gdiplus.h>
#include <string>
using namespace Gdiplus;

namespace ImageSources {
	class ImageSource {
	public:
		ImageSource() {}

		virtual Bitmap* Load(LPCTSTR loc = L"") {
			return NULL;
		};
	};
};

