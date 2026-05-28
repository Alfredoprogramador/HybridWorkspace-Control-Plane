// Package osquery provides device posture collection using osquery or native OS APIs.
package osquery

import (
	"context"
	"runtime"
)

// DevicePosture represents the security posture of a device.
type DevicePosture struct {
	DiskEncrypted     bool   `json:"disk_encrypted"`
	AntivirusEnabled  bool   `json:"antivirus_enabled"`
	OsUpToDate        bool   `json:"os_up_to_date"`
	FirewallEnabled   bool   `json:"firewall_enabled"`
	ScreenLockEnabled bool   `json:"screen_lock_enabled"`
	OsVersion         string `json:"os_version,omitempty"`
}

// PostureCollector collects device posture information.
type PostureCollector struct{}

// NewPostureCollector creates a new PostureCollector.
func NewPostureCollector() *PostureCollector {
	return &PostureCollector{}
}

// Collect gathers current device posture.
func (c *PostureCollector) Collect(_ context.Context) (*DevicePosture, error) {
	posture := &DevicePosture{
		OsVersion: runtime.GOOS + "/" + runtime.GOARCH,
	}

	switch runtime.GOOS {
	case "linux":
		collectLinuxPosture(posture)
	case "darwin":
		collectMacOSPosture(posture)
	case "windows":
		collectWindowsPosture(posture)
	default:
		// Unsupported OS: return conservative defaults
		posture.FirewallEnabled = false
		posture.DiskEncrypted = false
	}

	return posture, nil
}
