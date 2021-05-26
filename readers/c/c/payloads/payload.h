#pragma once
#include <Windows.h>

namespace Reader {
	class Payload {
	public:
		char* payload = NULL;

		Payload() {}

		Payload(char* p) {
			payload = p;
		}
		virtual void Run() {};
	};
}