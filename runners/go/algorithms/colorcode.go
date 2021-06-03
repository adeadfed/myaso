// +build payload_algorithm_colorcode

package algorithms

import (
	"image"
)

type ColorCode struct{}

func get_colorcode(target byte, source byte) byte {
	if source > 128 {
		return (target << 1) | 1
	} else {
		return (target << 1) | 0
	}
}

func (cc ColorCode) Read(img image.Image, payload_data []byte) {
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

				payload_data[pos/8] = get_colorcode(payload_data[pos/8], byte(channel))
				pos++
				length--
			}
		}
	}
}
