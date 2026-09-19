package milking

import (
	"errors"
	"fmt"
	"time"

	"holmdairy.example/byre/internal/env"
)

// Reading is one message from a parlour milk meter.
type Reading struct {
	Tag     string
	TakenAt time.Time
	Kg      float64
}

// MeterIngest receives readings from the parlour's milk meters and records
// each one as a milking.
type MeterIngest struct {
	// Withheld answers whether a cow is on the withhold list right now. It is
	// supplied by the treatment package when the program is wired up.
	Withheld func(e env.Env, tag string) bool

	// OnSessionOpen is called once when the first reading of a new session
	// arrives, before that reading is recorded.
	OnSessionOpen func(e env.Env, s Session)

	current Session
}

// ErrBadReading is returned for a reading no milking can be made from.
var ErrBadReading = errors.New("unusable meter reading")

// Accept records one reading as a milking. The reading is filed under the
// session it was taken in, worked out from TakenAt, even when that session
// has closed and a later one is open (docs/decisions/0002).
func (m *MeterIngest) Accept(e env.Env, r Reading) (Milking, error) {
	if r.Tag == "" || r.Kg <= 0 {
		return Milking{}, fmt.Errorf("%w: tag %q, %.1f kg", ErrBadReading, r.Tag, r.Kg)
	}
	if r.TakenAt.After(e.Clock.Now().Add(time.Minute)) {
		return Milking{}, fmt.Errorf("%w: %s taken in the future", ErrBadReading, r.Tag)
	}

	s := SessionAt(e, r.TakenAt)
	if s.Day.After(m.current.Day) || (s.Day.Equal(m.current.Day) && s.Slot != m.current.Slot && !m.isLate(e, r)) {
		m.current = s
		if m.OnSessionOpen != nil {
			m.OnSessionOpen(e, s)
		}
	}

	mk := Milking{
		Tag:      r.Tag,
		Session:  s,
		At:       r.TakenAt,
		YieldKg:  r.Kg,
		Withheld: m.Withheld != nil && m.Withheld(e, r.Tag),
	}
	_, err := e.DB.Exec(
		`INSERT INTO milkings (tag, day, slot, at, yield_kg, withheld) VALUES (?, ?, ?, ?, ?, ?)`,
		mk.Tag, mk.Session.Day, string(mk.Session.Slot), mk.At, mk.YieldKg, mk.Withheld,
	)
	if err != nil {
		return Milking{}, fmt.Errorf("record milking of %s: %w", mk.Tag, err)
	}
	return mk, nil
}

// isLate reports whether r was taken in a session earlier than the one now
// open, which is how a reading held back by the meters shows up.
func (m *MeterIngest) isLate(e env.Env, r Reading) bool {
	return SessionAt(e, r.TakenAt) != SessionAt(e, e.Clock.Now()) &&
		r.TakenAt.Before(e.Clock.Now())
}

// SessionTotals adds up the milkings recorded under s.
func SessionTotals(e env.Env, s Session) (Totals, error) {
	rows, err := e.DB.Query(`SELECT yield_kg, withheld FROM milkings WHERE day = ? AND slot = ?`, s.Day, string(s.Slot))
	if err != nil {
		return Totals{}, fmt.Errorf("totals for %s %s: %w", s.Day.Format(time.DateOnly), s.Slot, err)
	}
	defer rows.Close()

	var t Totals
	for rows.Next() {
		var mk Milking
		if err := rows.Scan(&mk.YieldKg, &mk.Withheld); err != nil {
			return Totals{}, err
		}
		t.Add(mk)
	}
	return t, rows.Err()
}
