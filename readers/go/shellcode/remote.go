// +build delivery_method_remote

package main

func get_image(url string) image.Image {
    resp, _ := http.Get(url)
	img_data, _ := ioutil.ReadAll(resp.Body)
	r := bytes.NewReader(img_data)

	img, _, _ := image.Decode(r)
	return img
}
