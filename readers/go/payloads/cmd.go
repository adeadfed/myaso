// +build payload_type_cmd

package payloads

import (
	"os/exec"
)

type cmd struct {
	exe  string
	args []string
}

func (c cmd) run() {
	cmd := exec.Command(c.exe, c.args...)
	cmd.Run()
}
