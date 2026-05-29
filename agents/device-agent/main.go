// Package main is the entry point for the HybridWorkspace device agent.
// The device agent runs on end-user devices and:
//   - Collects device posture information
//   - Reports posture to the Control Plane
//   - Enforces local policies
//   - Manages VPN connectivity via Tailscale
package main

import (
	"os"

	"github.com/alfredoprogramador/hwcp/device-agent/cmd"
)

func main() {
	if err := cmd.Execute(); err != nil {
		os.Exit(1)
	}
}
