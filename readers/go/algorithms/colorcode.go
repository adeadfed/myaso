// +build payload_algorithm_colorcode

package algorithms

import (
	"image"
)

func get_colorcode(b byte) byte {
    return 1 if b > 128 else 0
}

func GetPayload(img image.Image, payload_data []byte) {
	g := img.Bounds()

	height := g.Dy()
	width := g.Dx()

	length := len(payload_data) * 8
	pos := 0

	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {

			r, g, b, _ := img.At(j, i).RGBA()
            channel = r

            if length <= 0 {
                return
            }

            payload_data[pos/8] = get_colorcode(payload_data[pos/8], channel)
            pos++
            length--
		}
	}
}
