// +build delivery_method_remote

package main

import (
	"image"
    "io/ioutil"
	"net/http"

	_ "image/png"
	_ "golang.org/x/image/bmp"
)

func get_image(url string) image.Image {
    resp, _ := http.Get(url)
	img_data, _ := ioutil.ReadAll(resp.Body)
	r := bytes.NewReader(img_data)

	img, _, _ := image.Decode(r)
	return img
}