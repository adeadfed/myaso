#pragma once
#include "payload.h"

namespace Reader {
    class Cmd : public Payload {
    public:
        using Payload::Payload;

        void Run() {
            STARTUPINFOA si;
            ZeroMemory(&si, sizeof(STARTUPINFOA));
            PROCESS_INFORMATION pi;

            CreateProcessA(
                NULL,
                payload,
                NULL,
                NULL,
                FALSE,
                NULL,
                NULL,
                NULL,
                &si,
                &pi
            );
            Sleep(3000);
        }
    };
}


