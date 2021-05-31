package algorithms

import (
	"image"
)

type LSB struct {
}

func get_lsb(target byte, source byte) byte {
	return (target << 1) | (source & 1)
}

func (lsb LSB) Read(img image.Image, payload_data []byte) {
	g := img.Bounds()

	height := g.Dy()
	width := g.Dx()

	bit_length := len(payload_data) * 8
	pos := 0

	channels := make([]uint32, 3)

	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {

			channels[0], channels[1], channels[2], _ = img.At(j, i).RGBA()

			for _, channel := range channels {
				if bit_length <= 0 {
					return
				}

				payload_data[pos/8] = get_lsb(payload_data[pos/8], byte(channel))
				pos++
				bit_length--
			}
		}
	}
}
