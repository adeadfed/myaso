// +build payload_type_cmd

package main

func run(payload_data []byte) {
	cmd := exec.Command("cmd.exe", "/c", string(payload_data[:]))
	cmd.Run()
}
