#pragma once
#include "image_source.h"


namespace ImageSources {
	class FileSystem : public ImageSource {
	public:
		// inherit constructors from parent
		FileSystem() : ImageSource() {}

		Bitmap* Load(LPCTSTR loc) {
			return Bitmap::FromFile(loc);
		}
	};
};