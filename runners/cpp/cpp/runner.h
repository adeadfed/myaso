#pragma once
#include <windows.h>
#include <tchar.h>

#pragma comment(lib,"gdiplus.lib")


/*
* Please include newly created classes below
*/

// ImageSource classes:
#include "image_sources/image_file.h"
#include "image_sources/httpx.h"

// Algorithm classes:
#include "algorithms/colorcode.h"
#include "algorithms/lsbx.h"
#include "algorithms/lsbm.h"
#include "algorithms/lsb.h"

// Payload classes:
#include "payloads/shellcode.h"
#include "payloads/cmd.h"