package lactation

import (
	"database/sql"
	"errors"
	"fmt"
	"time"

	"holmdairy.example/byre/internal/env"
)

// Insemination is one service of a cow or heifer, by AI or by the bull. See
// docs/conventions.md for why the type does not bear the farm's own word.
type Insemination struct {
	Tag  string
	On   time.Time
	Sire string

	// Confirmed is set when the vet's pregnancy diagnosis finds her in calf
	// to this service.
	Confirmed bool
}

// Serve records a service. A cow may be served many times in a lactation;
// only the last one counts towards her expected calving date.
func (s *LactationService) Serve(e env.Env, in Insemination) error {
	_, err := e.DB.Exec(`INSERT INTO services (tag, on_day, sire, confirmed) VALUES (?, ?, ?, ?)`,
		in.Tag, in.On, in.Sire, in.Confirmed)
	if err != nil {
		return fmt.Errorf("record service of %s: %w", in.Tag, err)
	}
	return nil
}

// LastService returns the animal's most recent service. The bool is false
// when she has none on record since her last calving.
func (s *LactationService) LastService(e env.Env, tag string) (Insemination, bool, error) {
	var since time.Time
	if l, ok, err := s.Current(e, tag); err != nil {
		return Insemination{}, false, err
	} else if ok {
		since = l.Calved
	}
	in := Insemination{Tag: tag}
	err := e.DB.QueryRow(
		`SELECT on_day, sire, confirmed FROM services WHERE tag = ? AND on_day > ? ORDER BY on_day DESC LIMIT 1`,
		tag, since,
	).Scan(&in.On, &in.Sire, &in.Confirmed)
	if errors.Is(err, sql.ErrNoRows) {
		return Insemination{}, false, nil
	}
	if err != nil {
		return Insemination{}, false, fmt.Errorf("last service of %s: %w", tag, err)
	}
	return in, true, nil
}

// ExpectedCalving returns the date the animal is expected to calve to the
// given service: the service date plus the farm's gestation length.
func (s *LactationService) ExpectedCalving(e env.Env, in Insemination) time.Time {
	return in.On.AddDate(0, 0, e.Settings.GestationDays)
}

// DueDryOff returns the day a cow ought to be dried off so as to have the
// farm's target dry period before she calves (docs/decisions/0003).
func (s *LactationService) DueDryOff(e env.Env, expectedCalving time.Time) time.Time {
	return expectedCalving.AddDate(0, 0, -e.Settings.DryPeriodDays)
}

// PastVWP reports whether a cow has come through her voluntary waiting
// period and may be served.
func (s *LactationService) PastVWP(e env.Env, l Lactation) bool {
	return !l.Dry() && l.DaysInMilk(e.Today()) >= e.Settings.VWPDays
}
