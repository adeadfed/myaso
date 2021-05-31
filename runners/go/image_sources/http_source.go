// +build delivery_method_remote

package image_sources

import (
	"bytes"
	"image"
	"io/ioutil"
	"net/http"

	_ "image/png"

	_ "golang.org/x/image/bmp"
)

type http_source struct {
	location string
}

func (hs http_source) get_image() image.Image {
	resp, _ := http.Get(hs.location)

	img_data, _ := ioutil.ReadAll(resp.Body)
	r := bytes.NewReader(img_data)

	img, _, _ := image.Decode(r)
	return img
}
