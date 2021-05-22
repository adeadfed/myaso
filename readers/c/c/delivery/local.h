#pragma once
#include "delivery.h"


namespace Reader {
	class Local : public Delivery {
	public:
		// inherit constructors from parent
		Local(LPCTSTR loc) : Delivery(loc) { }
		Local() : Delivery() {}

		void loadImage() {
			bm = Bitmap::FromFile(location.c_str());
		}
	};
};