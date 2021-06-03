package payloads

import (
	"os/exec"
	"strings"
)

type Cmd struct{}

func (c Cmd) Run(payload_data []byte) {
	payload_args := strings.Split(string(payload_data), " ")

	cmd := exec.Command(payload_args[0], payload_args[1:]...)
	cmd.Run()
}
