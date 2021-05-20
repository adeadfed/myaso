// +build payload_type_cmd

package payload_types

import (
	"os"
	"os/exec"
)

func Run(payload_data []byte) {
	cmd := exec.Command("cmd.exe", "/c", string(payload_data[:]))
	cmd.Run()
}
