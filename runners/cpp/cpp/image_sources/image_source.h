#pragma once
#include <windows.h>
#include <gdiplus.h>
#include <string>
using namespace Gdiplus;

namespace ImageSources {
	class ImageSource {
	public:
		ImageSource() {}

		virtual Bitmap* Load(const wchar_t* loc = L"") {
			return NULL;
		};
	};
};

