// Package milking records milkings as they come in from the parlour and
// adds them up by session.
package milking

import (
	"time"

	"holmdairy.example/byre/internal/env"
)

// Slot is the place of a session in the day.
type Slot string

const (
	AM     Slot = "am"
	Midday Slot = "midday"
	PM     Slot = "pm"
)

// Session says which session is meant: a day and a slot. It is a key for
// looking milkings up and nothing more; it has no state and no behaviour.
type Session struct {
	Day  time.Time
	Slot Slot
}

// Milking is one cow milked once.
type Milking struct {
	Tag     string
	Session Session
	At      time.Time
	YieldKg float64

	// Withheld is set when the cow was on the withhold list. The yield is
	// recorded all the same, but is left out of the saleable total.
	Withheld bool
}

// SessionAt returns the session a moment falls in. On twice-a-day farms the
// day splits at noon; on three-times-a-day farms at 10:00 and 17:00.
func SessionAt(e env.Env, at time.Time) Session {
	day := time.Date(at.Year(), at.Month(), at.Day(), 0, 0, 0, 0, at.Location())
	hour := at.Hour()
	if e.Settings.SessionsPerDay == 3 {
		switch {
		case hour < 10:
			return Session{Day: day, Slot: AM}
		case hour < 17:
			return Session{Day: day, Slot: Midday}
		default:
			return Session{Day: day, Slot: PM}
		}
	}
	if hour < 12 {
		return Session{Day: day, Slot: AM}
	}
	return Session{Day: day, Slot: PM}
}

// Totals is what a session adds up to.
type Totals struct {
	Cows       int
	SaleableKg float64
	WithheldKg float64
}

// Add folds one milking into the totals.
func (t *Totals) Add(m Milking) {
	t.Cows++
	if m.Withheld {
		t.WithheldKg += m.YieldKg
		return
	}
	t.SaleableKg += m.YieldKg
}
