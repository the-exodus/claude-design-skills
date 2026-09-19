// Package lactation follows each cow round her cycle: calving, lactation,
// dry off, the dry period, and calving again.
package lactation

import (
	"database/sql"
	"errors"
	"fmt"
	"time"

	"holmdairy.example/byre/internal/env"
	"holmdairy.example/byre/internal/herd"
)

// ShortDryPeriodDays is the length under which a dry period counts as short.
// A cow whose dry period will be shorter than 40 days is marked as short on
// the calving list.
const ShortDryPeriodDays = 40

// Lactation is one lactation of one cow, from the calving that opened it to
// the dry off that closed it.
type Lactation struct {
	Tag    string
	Parity int
	Calved time.Time

	// DriedOff is the day of the dry off. Nil while she is still milking.
	DriedOff *time.Time
}

// Dry reports whether the lactation has ended, so that the cow is in her
// dry period.
func (l Lactation) Dry() bool {
	return l.DriedOff != nil
}

// DaysInMilk returns the days since calving on the given day, or zero for a
// dry cow and for an animal that has never calved.
func (l Lactation) DaysInMilk(on time.Time) int {
	if l.Dry() || l.Calved.IsZero() {
		return 0
	}
	return int(on.Sub(l.Calved).Hours() / 24)
}

// LactationService records calvings and dry offs and answers questions about
// where a cow is in her cycle.
type LactationService struct {
	store *herd.HerdStore
}

// NewLactationService returns the service over the given herd store.
func NewLactationService(store *herd.HerdStore) *LactationService {
	return &LactationService{store: store}
}

// ErrNotMilking is returned when a dry off is recorded for an animal with no
// open lactation.
var ErrNotMilking = errors.New("animal has no open lactation")

// Calve records a calving. It raises the animal's parity by one, which is
// what turns a heifer into a cow, and opens a new lactation.
func (s *LactationService) Calve(e env.Env, tag string, on time.Time) (Lactation, error) {
	a, err := s.store.Get(e, tag)
	if err != nil {
		return Lactation{}, err
	}
	if a.Sex != herd.Female {
		return Lactation{}, fmt.Errorf("calving for %s: not a female", tag)
	}
	a.Parity++
	if err := s.store.Put(e, a); err != nil {
		return Lactation{}, err
	}
	l := Lactation{Tag: tag, Parity: a.Parity, Calved: on}
	_, err = e.DB.Exec(`INSERT INTO lactations (tag, parity, calved) VALUES (?, ?, ?)`, l.Tag, l.Parity, l.Calved)
	if err != nil {
		return Lactation{}, fmt.Errorf("open lactation for %s: %w", tag, err)
	}
	return l, nil
}

// DryOff records the dry off of a cow, which closes her lactation and starts
// her dry period.
func (s *LactationService) DryOff(e env.Env, tag string, on time.Time) (Lactation, error) {
	l, ok, err := s.Current(e, tag)
	if err != nil {
		return Lactation{}, err
	}
	if !ok || l.Dry() {
		return Lactation{}, fmt.Errorf("dry off %s: %w", tag, ErrNotMilking)
	}
	l.DriedOff = &on
	_, err = e.DB.Exec(`UPDATE lactations SET dried_off = ? WHERE tag = ? AND parity = ?`, on, l.Tag, l.Parity)
	if err != nil {
		return Lactation{}, fmt.Errorf("dry off %s: %w", tag, err)
	}
	return l, nil
}

// Current returns the animal's latest lactation, open or closed. The bool is
// false for an animal that has never calved.
func (s *LactationService) Current(e env.Env, tag string) (Lactation, bool, error) {
	l := Lactation{Tag: tag}
	var dried sql.NullTime
	err := e.DB.QueryRow(
		`SELECT parity, calved, dried_off FROM lactations WHERE tag = ? ORDER BY parity DESC LIMIT 1`, tag,
	).Scan(&l.Parity, &l.Calved, &dried)
	if errors.Is(err, sql.ErrNoRows) {
		return Lactation{}, false, nil
	}
	if err != nil {
		return Lactation{}, false, fmt.Errorf("lactation of %s: %w", tag, err)
	}
	if dried.Valid {
		l.DriedOff = &dried.Time
	}
	return l, true, nil
}
