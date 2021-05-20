#include <gdiplus.h>
#include <Windows.h>
#include <winhttp.h>
#include <string>

using namespace Gdiplus;

#pragma comment(lib, "winhttp.lib")


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
