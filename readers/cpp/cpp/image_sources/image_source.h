#pragma once
#include <Windows.h>
#include <gdiplus.h>
#include <string>
using namespace Gdiplus;

namespace ImageSources {
	class ImageSource {
	public:
		std::wstring location;

		ImageSource(LPCTSTR loc = L"") {
			location = loc;
		}

		virtual Bitmap* loadImage() {
			return NULL;
		};
	};
};

