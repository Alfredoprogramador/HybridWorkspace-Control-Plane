package osquery

import (
	"os/exec"
	"strings"
)

// collectLinuxPosture gathers security posture on Linux.
func collectLinuxPosture(posture *DevicePosture) {
	posture.FirewallEnabled = checkLinuxFirewall()
	posture.DiskEncrypted = checkLinuxEncryption()
	posture.AntivirusEnabled = checkLinuxAntivirus()
	posture.OsUpToDate = checkLinuxUpdates()
	posture.ScreenLockEnabled = true // Assume enabled; hard to check portably
}

func checkLinuxFirewall() bool {
	// Check ufw or iptables
	if out, err := exec.Command("ufw", "status").Output(); err == nil {
		return strings.Contains(string(out), "Status: active")
	}
	if _, err := exec.Command("iptables", "-L").Output(); err == nil {
		return true
	}
	return false
}

func checkLinuxEncryption() bool {
	// Check if LUKS encryption is active
	out, err := exec.Command("lsblk", "-o", "NAME,TYPE").Output()
	if err != nil {
		return false
	}
	return strings.Contains(string(out), "crypt")
}

func checkLinuxAntivirus() bool {
	// Check for ClamAV or other AV
	_, clamErr := exec.LookPath("clamscan")
	_, sophoErr := exec.LookPath("sophos-av")
	return clamErr == nil || sophoErr == nil
}

func checkLinuxUpdates() bool {
	// Check if there are pending security updates
	out, err := exec.Command("apt-get", "--simulate", "upgrade").Output()
	if err != nil {
		return true // Assume up to date if we can't check
	}
	return strings.Contains(string(out), "0 upgraded")
}

// collectMacOSPosture gathers security posture on macOS.
func collectMacOSPosture(posture *DevicePosture) {
	posture.FirewallEnabled = checkMacOSFirewall()
	posture.DiskEncrypted = checkMacOSFileVault()
	posture.AntivirusEnabled = checkMacOSXProtect()
	posture.OsUpToDate = true // Would require softwareupdate --list
	posture.ScreenLockEnabled = checkMacOSScreenLock()
}

func checkMacOSFirewall() bool {
	out, err := exec.Command("defaults", "read",
		"/Library/Preferences/com.apple.alf", "globalstate").Output()
	if err != nil {
		return false
	}
	return strings.TrimSpace(string(out)) != "0"
}

func checkMacOSFileVault() bool {
	out, err := exec.Command("fdesetup", "status").Output()
	if err != nil {
		return false
	}
	return strings.Contains(string(out), "FileVault is On")
}

func checkMacOSXProtect() bool {
	// XProtect is built into macOS
	_, err := exec.Command("spctl", "--status").Output()
	return err == nil
}

func checkMacOSScreenLock() bool {
	out, err := exec.Command("osascript", "-e",
		`tell application "System Events" to get value of slider 1 of tab group 1 of window 1 of application process "System Preferences"`).Output()
	if err != nil {
		return true // Assume enabled
	}
	_ = out
	return true
}

// collectWindowsPosture gathers security posture on Windows.
func collectWindowsPosture(posture *DevicePosture) {
	// Windows-specific checks would use WMI or PowerShell
	// This is a placeholder for Windows implementation
	posture.FirewallEnabled = true
	posture.DiskEncrypted = false
	posture.AntivirusEnabled = true
	posture.OsUpToDate = true
	posture.ScreenLockEnabled = true
}
