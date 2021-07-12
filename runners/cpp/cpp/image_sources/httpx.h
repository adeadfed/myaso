#pragma once
#include "image_source.h"
#include <winhttp.h>
#pragma comment(lib, "winhttp.lib")

namespace ImageSources {
    class HttpX: public ImageSource {
        int port = 0;
        int request_flags = 0;
        std::wstring host;
        std::wstring path;

    public:
        // inherit constructors from parent
        HttpX() : ImageSource() {}

        Bitmap* Load(std::wstring uri) {
            // parse the request URI
            parseUri(uri);

            // make request and load image in string
            std::string request_data = doHttpRequest();
           
            // allocate a global buffer
            HGLOBAL request_gl_buffer = GlobalAlloc(GMEM_MOVEABLE, request_data.size() + 1);
            LPVOID request_buffer = GlobalLock(request_gl_buffer);

            // copy image from string to global buffer
            CopyMemory(request_buffer, request_data.c_str(), request_data.size() + 1);

            // init a stream from global buffer
            IStream* image_stream = NULL;
            CreateStreamOnHGlobal(request_buffer, FALSE, &image_stream);
            
            // create image from buffer
            return Bitmap::FromStream(image_stream);
        }
    private:
        std::string doHttpRequest() {
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
                host.c_str(),
                port,
                0
            );

            hRequest = WinHttpOpenRequest(
                hConnect,
                L"GET",
                path.c_str(),
                NULL,
                WINHTTP_NO_REFERER,
                WINHTTP_DEFAULT_ACCEPT_TYPES,
                request_flags
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

            return data;
        }

        void parseUri(std::wstring uri) {
            size_t proto_pos = uri.find(L"://");
            std::wstring proto = uri.substr(0, proto_pos);
            uri = uri.substr(proto_pos + proto.length() - 1, std::wstring::npos);

            proto == L"https://" ? request_flags = WINHTTP_FLAG_SECURE : request_flags = 0;

            size_t path_pos = uri.find(L"/");
            path = uri.substr(path_pos, std::wstring::npos);
            uri = uri.substr(0, path_pos);

            size_t port_pos = uri.find(L":");
            if (port_pos == std::wstring::npos) {
                host = uri;
                request_flags ? port = 443 : port = 80;
            }
            else {
                host = uri.substr(0, port_pos);
                port = std::stoi(uri.substr(port_pos + 1, std::wstring::npos));
            } 
        }
    };
}


