// +build delivery_method_local

package image_sources

import (
	"image"
	"os"

	_ "image/png"

	_ "golang.org/x/image/bmp"
)

type file_source struct {
	location string
}

func (fs file_source) get_image() image.Image {
	img_file, _ := os.Open(fs.location)
	img, _, _ := image.Decode(img_file)
	return img
}
