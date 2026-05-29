// Package cmd provides the CLI commands for the device agent.
package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var cfgFile string

var rootCmd = &cobra.Command{
	Use:   "hwcp-agent",
	Short: "HybridWorkspace Control Plane Device Agent",
	Long: `The HWCP Device Agent runs on end-user devices and provides:
  - Continuous security posture monitoring
  - Zero Trust policy enforcement
  - Automatic VPN connectivity (Tailscale)
  - Secure communication with the Control Plane`,
}

// Execute runs the root command.
func Execute() error {
	return rootCmd.Execute()
}

func init() {
	cobra.OnInitialize(initConfig)
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default: /etc/hwcp/agent.yaml)")
	rootCmd.AddCommand(startCmd)
	rootCmd.AddCommand(enrollCmd)
	rootCmd.AddCommand(statusCmd)
	rootCmd.AddCommand(versionCmd)
}

func initConfig() {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	} else {
		viper.AddConfigPath("/etc/hwcp")
		viper.AddConfigPath("$HOME/.hwcp")
		viper.SetConfigName("agent")
		viper.SetConfigType("yaml")
	}
	viper.SetEnvPrefix("HWCP")
	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err == nil {
		fmt.Fprintln(os.Stderr, "Using config file:", viper.ConfigFileUsed())
	}
}
