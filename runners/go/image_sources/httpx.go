package image_sources

import (
	"bytes"
	"image"
	"io/ioutil"
	"net/http"

	_ "image/png"

	_ "golang.org/x/image/bmp"
)

type HttpX struct {
}

func (hx HttpX) Load(location string) image.Image {
	resp, _ := http.Get(location)

	img_data, _ := ioutil.ReadAll(resp.Body)
	r := bytes.NewReader(img_data)

	img, _, _ := image.Decode(r)
	return img
}
