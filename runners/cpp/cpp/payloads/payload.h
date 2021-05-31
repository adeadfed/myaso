#pragma once
#include <Windows.h>

namespace Payloads {
	class Payload {
	public:

		Payload() {}

		virtual void Run(uint8_t * p, int n) {};
	};
}