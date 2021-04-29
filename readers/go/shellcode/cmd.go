// +build payload_type_cmd

package main

import (
	"os"
	"os/exec"
)

func run(payload_data []byte) {
	cmd := exec.Command("cmd.exe", "/c", string(payload_data[:]))
	cmd.Run()
}
