#pragma once
#include "image_source.h"


namespace ImageSources {
	class FileSystem : public ImageSource {
	public:
		// inherit constructors from parent
		FileSystem(LPCTSTR loc) : ImageSource(loc) { }
		FileSystem() : ImageSource() {}

		Bitmap* loadImage() {
			return Bitmap::FromFile(location.c_str());
		}
	};
};