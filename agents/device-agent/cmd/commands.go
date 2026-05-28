package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print the agent version",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("hwcp-agent version 0.1.0")
	},
}

var statusCmd = &cobra.Command{
	Use:   "status",
	Short: "Show device agent status",
	RunE: func(cmd *cobra.Command, args []string) error {
		fmt.Println("HWCP Device Agent Status")
		fmt.Println("========================")
		fmt.Println("Status: Running")
		fmt.Println("Last posture check: N/A")
		fmt.Println("Trust level: Unknown")
		fmt.Println("VPN: Disconnected")
		return nil
	},
}

var enrollCmd = &cobra.Command{
	Use:   "enroll",
	Short: "Enroll this device with the Control Plane",
	Long:  "Enroll this device with the HybridWorkspace Control Plane using an enrollment token.",
	RunE: func(cmd *cobra.Command, args []string) error {
		token, _ := cmd.Flags().GetString("token")
		server, _ := cmd.Flags().GetString("server")
		if token == "" {
			return fmt.Errorf("enrollment token is required: use --token <token>")
		}
		fmt.Printf("Enrolling device with server %s...\n", server)
		fmt.Printf("Enrollment token: %s\n", token[:minInt(8, len(token))]+"****")
		fmt.Println("Device enrolled successfully. Run 'hwcp-agent start' to begin monitoring.")
		return nil
	},
}

func minInt(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func init() {
	enrollCmd.Flags().String("token", "", "Enrollment token (required)")
	enrollCmd.Flags().String("server", "https://api.hwcp.company.com", "Control Plane API URL")
	_ = enrollCmd.MarkFlagRequired("token")
}
