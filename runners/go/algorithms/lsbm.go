package algorithms

import (
	"image"
)

type LSBM struct{}

func get_lsbm(target byte, source byte) byte {
	return (target << 1) | (source % 2)
}

func (lsbm LSBM) Read(img image.Image, payload_data []byte) {
	g := img.Bounds()

	height := g.Dy()
	width := g.Dx()

	length := len(payload_data) * 8
	pos := 0

	channels := make([]uint32, 3)

	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {

			channels[0], channels[1], channels[2], _ = img.At(j, i).RGBA()

			for _, channel := range channels {
				if length <= 0 {
					return
				}

				payload_data[pos/8] = get_lsbm(payload_data[pos/8], byte(channel))
				pos++
				length--
			}
		}
	}
}
