#pragma once
#include "image_source.h"


namespace ImageSources {
	class ImageFile : public ImageSource {
	public:
		// inherit constructors from parent
		ImageFile() : ImageSource() {}

		Bitmap* Load(const wchar_t* loc) {
			return Bitmap::FromFile(loc);
		}
	};
};