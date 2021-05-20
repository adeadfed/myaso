#include <Windows.h>

void run(char* payload_data, int payload_bits) {
    STARTUPINFOA si;
    ZeroMemory(&si, sizeof(STARTUPINFOA));
    PROCESS_INFORMATION pi;

    CreateProcessA(
        NULL,
        payload_data,
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

