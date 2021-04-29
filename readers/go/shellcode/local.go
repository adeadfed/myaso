// +build delivery_method_local

package main

func get_image(filename string) image.Image {
	img_file, _ := os.Open(filename)
	img, _, _ := image.Decode(img_file)
	return img
}
