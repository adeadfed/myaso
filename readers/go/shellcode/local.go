// +build delivery_method_local

package main

import (
	"image"
)

func get_image(filename string) image.Image {
	img_file, _ := os.Open(filename)
	img, _, _ := image.Decode(img_file)
	return img
}
