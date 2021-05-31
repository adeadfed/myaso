// +build delivery_method_local

package delivery_methods

import (
    "os"
//     "log"
	"image"

	_ "image/png"
	_ "golang.org/x/image/bmp"
)

func GetImage(filename string) image.Image {
	img_file, _ := os.Open(filename)
// 	if err != nil {
// 	    log.Fatal(err)
// 	}
	img, _, _ := image.Decode(img_file)
//     if err != nil {
// 		log.Fatal(err)
// 	}
	return img
}
