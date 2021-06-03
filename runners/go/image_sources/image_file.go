package image_sources

import (
	"image"
	"os"

	_ "image/png"

	_ "golang.org/x/image/bmp"
)

type ImageFile struct {
}

func (im ImageFile) Load(location string) image.Image {
	img_file, _ := os.Open(location)
	img, _, _ := image.Decode(img_file)
	return img
}
