// Package telemetry handles sending posture reports to the Control Plane.
package telemetry

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/alfredoprogramador/hwcp/device-agent/internal/osquery"
)

// PostureReporter sends posture data to the Control Plane API.
type PostureReporter struct {
	serverURL string
	token     string
	deviceID  string
	client    *http.Client
}

// NewPostureReporter creates a new PostureReporter.
func NewPostureReporter(serverURL, token, deviceID string) *PostureReporter {
	return &PostureReporter{
		serverURL: serverURL,
		token:     token,
		deviceID:  deviceID,
		client: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

type posturePayload struct {
	DiskEncrypted     bool   `json:"disk_encrypted"`
	AntivirusEnabled  bool   `json:"antivirus_enabled"`
	OsUpToDate        bool   `json:"os_up_to_date"`
	FirewallEnabled   bool   `json:"firewall_enabled"`
	ScreenLockEnabled bool   `json:"screen_lock_enabled"`
	OsVersion         string `json:"os_version,omitempty"`
}

// Report sends the device posture to the Control Plane.
func (r *PostureReporter) Report(ctx context.Context, posture *osquery.DevicePosture) error {
	payload := posturePayload{
		DiskEncrypted:     posture.DiskEncrypted,
		AntivirusEnabled:  posture.AntivirusEnabled,
		OsUpToDate:        posture.OsUpToDate,
		FirewallEnabled:   posture.FirewallEnabled,
		ScreenLockEnabled: posture.ScreenLockEnabled,
		OsVersion:         posture.OsVersion,
	}

	body, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("marshaling posture: %w", err)
	}

	url := fmt.Sprintf("%s/api/v1/devices/%s/posture", r.serverURL, r.deviceID)
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(body))
	if err != nil {
		return fmt.Errorf("creating request: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+r.token)

	resp, err := r.client.Do(req)
	if err != nil {
		return fmt.Errorf("sending posture report: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return fmt.Errorf("server returned status %d", resp.StatusCode)
	}

	return nil
}
