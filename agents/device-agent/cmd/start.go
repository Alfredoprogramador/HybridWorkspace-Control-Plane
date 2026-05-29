package cmd

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/alfredoprogramador/hwcp/device-agent/internal/osquery"
	"github.com/alfredoprogramador/hwcp/device-agent/internal/telemetry"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var startCmd = &cobra.Command{
	Use:   "start",
	Short: "Start the device agent",
	Long:  "Start the HWCP device agent daemon. It will continuously monitor device posture and report to the Control Plane.",
	RunE:  runStart,
}

func init() {
	startCmd.Flags().Duration("interval", 15*time.Minute, "Posture check interval")
	startCmd.Flags().String("server", "https://api.hwcp.company.com", "Control Plane API URL")
}

func runStart(cmd *cobra.Command, args []string) error {
	interval, _ := cmd.Flags().GetDuration("interval")
	server := viper.GetString("server_url")
	if s, _ := cmd.Flags().GetString("server"); s != "" {
		server = s
	}

	token := viper.GetString("device_token")
	deviceID := viper.GetString("device_id")

	if token == "" || deviceID == "" {
		return fmt.Errorf("device not enrolled: run 'hwcp-agent enroll' first")
	}

	fmt.Printf("Starting HWCP device agent (device_id=%s, server=%s, interval=%s)\n",
		deviceID, server, interval)

	reporter := telemetry.NewPostureReporter(server, token, deviceID)
	collector := osquery.NewPostureCollector()

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Handle graceful shutdown
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	// Initial posture check on startup
	if err := reportPosture(ctx, collector, reporter); err != nil {
		fmt.Fprintf(os.Stderr, "Warning: initial posture report failed: %v\n", err)
	}

	for {
		select {
		case <-ticker.C:
			if err := reportPosture(ctx, collector, reporter); err != nil {
				fmt.Fprintf(os.Stderr, "Warning: posture report failed: %v\n", err)
			}
		case sig := <-sigCh:
			fmt.Printf("Received signal %v, shutting down...\n", sig)
			return nil
		case <-ctx.Done():
			return nil
		}
	}
}

func reportPosture(ctx context.Context, collector *osquery.PostureCollector, reporter *telemetry.PostureReporter) error {
	posture, err := collector.Collect(ctx)
	if err != nil {
		return fmt.Errorf("collecting posture: %w", err)
	}
	return reporter.Report(ctx, posture)
}
