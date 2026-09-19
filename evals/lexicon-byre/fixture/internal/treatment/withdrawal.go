// Package treatment records veterinary treatments and the withdrawals that
// follow them.
package treatment

import (
	"fmt"
	"time"

	"holmdairy.example/byre/internal/env"
)

// WithdrawalKind says what a withdrawal applies to (docs/decisions/0001).
type WithdrawalKind int

const (
	// MilkWithdrawal keeps the cow's milk out of the saleable total.
	MilkWithdrawal WithdrawalKind = iota
	// MeatWithdrawal bars the animal from sale for slaughter, not her milk.
	MeatWithdrawal
)

// Treatment is one course of a product given to one animal.
type Treatment struct {
	Tag, Product, Batch, GivenBy string
	// LastDose is when the last dose of the course was given.
	LastDose time.Time

	// MilkHours and MeatDays are the withdrawal figures from the vet or the
	// data sheet. Zero means the product carries none of that kind.
	MilkHours, MeatDays int
}

// Withdrawal is one open or past withdrawal on one animal.
type Withdrawal struct {
	Tag     string
	Kind    WithdrawalKind
	Product string
	Ends    time.Time
}

// TreatmentService records treatments and knows which animals are under
// which kind of withdrawal. The zero value is ready to use.
type TreatmentService struct {
	withheld map[string]Withdrawal
}

// Record stores a treatment and opens the withdrawals it carries, each
// running from the last dose. A cow given a product with a milk withdrawal
// goes on the withhold list at once, without waiting for the next session.
func (s *TreatmentService) Record(e env.Env, t Treatment) ([]Withdrawal, error) {
	var opened []Withdrawal
	if t.MilkHours > 0 {
		opened = append(opened, Withdrawal{t.Tag, MilkWithdrawal, t.Product, t.LastDose.Add(time.Duration(t.MilkHours) * time.Hour)})
	}
	if t.MeatDays > 0 {
		opened = append(opened, Withdrawal{t.Tag, MeatWithdrawal, t.Product, t.LastDose.AddDate(0, 0, t.MeatDays)})
	}
	for _, w := range opened {
		_, err := e.DB.Exec(`INSERT INTO withdrawals (tag, kind, product, ends) VALUES (?, ?, ?, ?)`,
			w.Tag, int(w.Kind), w.Product, w.Ends)
		if err != nil {
			return nil, fmt.Errorf("open withdrawal on %s: %w", t.Tag, err)
		}
	}
	return opened, s.sweepWithheld(e)
}

// Open returns every animal's open withdrawals, by ear tag. Where an animal
// has several of one kind, only the one that ends last is returned.
func (s *TreatmentService) Open(e env.Env) (map[string][]Withdrawal, error) {
	rows, err := e.DB.Query(
		`SELECT tag, kind, product, MAX(ends) FROM withdrawals WHERE ends > ? GROUP BY tag, kind`, e.Clock.Now())
	if err != nil {
		return nil, fmt.Errorf("open withdrawals: %w", err)
	}
	defer rows.Close()

	open := map[string][]Withdrawal{}
	for rows.Next() {
		var w Withdrawal
		if err := rows.Scan(&w.Tag, &w.Kind, &w.Product, &w.Ends); err != nil {
			return nil, err
		}
		open[w.Tag] = append(open[w.Tag], w)
	}
	return open, rows.Err()
}

// sweepWithheld rebuilds the set of withheld cows from the open withdrawals
// (glossary: withhold sweep). It runs when a session opens and after every
// treatment, so the withhold list is complete before the first cow is milked.
func (s *TreatmentService) sweepWithheld(e env.Env) error {
	open, err := s.Open(e)
	if err != nil {
		return err
	}
	withheld := map[string]Withdrawal{}
	for tag, ws := range open {
		for _, w := range ws {
			if w.Kind != MilkWithdrawal {
				continue
			}
			withheld[tag] = w
		}
	}
	s.withheld = withheld
	return nil
}

// OpenSession brings the withhold list up to date for a session about to start.
func (s *TreatmentService) OpenSession(e env.Env) error { return s.sweepWithheld(e) }

// Withheld reports whether the cow's milk is to be kept out of the tank.
func (s *TreatmentService) Withheld(e env.Env, tag string) bool {
	w, ok := s.withheld[tag]
	return ok && w.Ends.After(e.Clock.Now())
}

// WithholdList returns the milk withdrawal behind each withheld cow.
func (s *TreatmentService) WithholdList() map[string]Withdrawal { return s.withheld }
