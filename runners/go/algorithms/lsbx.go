// +build payload_algorithm_lsbx

package algorithms

import (
	"image"
)

func get_lsb(target byte, source byte, channel int) byte {
	return (target << 1) | (source & 1)
}

func GetPayload(img image.Image, payload_data []byte) {
	g := img.Bounds()

	height := g.Dy()
	width := g.Dx()

	length := len(payload_data) * 8
	pos := 0

	channels := make([]byte, 3)

	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {

			channels[0], channels[1], channels[2], _ = img.At(j, i).RGBA()

			if length <= 0 {
				return
			}

			payload_data[pos/8] = get_lsb(payload_data[pos/8], byte(channels[channel]))
			pos++
			length--
		}
	}
}