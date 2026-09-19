// Package env holds what every operation in Byre is handed: the farm's
// settings, the clock and the database handle.
package env

import (
	"database/sql"
	"fmt"
	"log/slog"
	"os"
	"time"

	"gopkg.in/yaml.v3"
)

// DefaultDryPeriodDays is the target dry period a new farm starts with. This
// default has history; do not change it without asking the herd manager.
const DefaultDryPeriodDays = 60

// Defaults for the remaining settings. docs/configuration.md lists them.
const (
	DefaultSessionsPerDay      = 2
	DefaultSessionCloseMinutes = 45
	DefaultGestationDays       = 283
	DefaultDryOffNoticeDays    = 7
	DefaultVWPDays             = 50
	DefaultCloseUpDays         = 21
)

// Settings is the farm's configuration as read from byre.yaml.
type Settings struct {
	HerdName            string   `yaml:"herd_name"`
	SessionsPerDay      int      `yaml:"sessions_per_day"`
	SessionCloseMinutes int      `yaml:"session_close_minutes"`
	GestationDays       int      `yaml:"gestation_days"`
	DryPeriodDays       int      `yaml:"dry_period_days"`
	DryOffNoticeDays    int      `yaml:"dry_off_notice_days"`
	VWPDays             int      `yaml:"vwp_days"`
	CloseUpDays         int      `yaml:"close_up_days"`
	Groups              []string `yaml:"groups"`
}

// Clock tells the time. The running service uses the wall clock; everything
// else can be handed a fixed one.
type Clock interface {
	Now() time.Time
}

// Env is handed as the first argument to every operation that needs a
// setting, the time or the database (glossary: Env).
type Env struct {
	Settings Settings
	Clock    Clock
	DB       *sql.DB
	Log      *slog.Logger
}

// Today returns the current farm-local calendar day, at midnight.
func (e Env) Today() time.Time {
	now := e.Clock.Now()
	return time.Date(now.Year(), now.Month(), now.Day(), 0, 0, 0, 0, now.Location())
}

// Defaults returns the settings a farm gets before byre.yaml is read.
func Defaults() Settings {
	return Settings{
		SessionsPerDay:      DefaultSessionsPerDay,
		SessionCloseMinutes: DefaultSessionCloseMinutes,
		GestationDays:       DefaultGestationDays,
		DryPeriodDays:       DefaultDryPeriodDays,
		DryOffNoticeDays:    DefaultDryOffNoticeDays,
		VWPDays:             DefaultVWPDays,
		CloseUpDays:         DefaultCloseUpDays,
		Groups:              []string{"milkers", "dry", "close-up", "heifers"},
	}
}

// Load reads byre.yaml over the defaults, so that a key the farm leaves out
// keeps its default.
func Load(path string) (Settings, error) {
	s := Defaults()
	raw, err := os.ReadFile(path)
	if err != nil {
		return s, fmt.Errorf("read settings %s: %w", path, err)
	}
	if err := yaml.Unmarshal(raw, &s); err != nil {
		return s, fmt.Errorf("parse settings %s: %w", path, err)
	}
	if s.SessionsPerDay != 2 && s.SessionsPerDay != 3 {
		return s, fmt.Errorf("sessions_per_day must be 2 or 3, got %d", s.SessionsPerDay)
	}
	return s, nil
}
