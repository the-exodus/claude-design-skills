// Package lists builds the lists the herd manager works from each day.
package lists

import (
	"sort"
	"time"

	"holmdairy.example/byre/internal/env"
	"holmdairy.example/byre/internal/herd"
	"holmdairy.example/byre/internal/lactation"
	"holmdairy.example/byre/internal/treatment"
)

// Row is one animal on one list.
type Row struct {
	Animal herd.Animal
	DIM    int
	Due    time.Time
	Note   string
}

// ListBuilder builds the daily lists from the records as they stand, afresh each time.
type ListBuilder struct {
	Herd       *herd.HerdStore
	Lactations *lactation.LactationService
	Treatments *treatment.TreatmentService
}

// Withhold lists every cow whose milk is being kept out of the tank, and until when.
func (b *ListBuilder) Withhold(e env.Env) ([]Row, error) {
	held := b.Treatments.WithholdList()
	return b.pick(e, func(s subject, row *Row) bool {
		w, ok := held[s.a.Tag]
		row.Due, row.Note = w.Ends, w.Product
		return ok
	})
}

// DryOff lists the cows due to be dried off within the farm's notice,
// soonest first. Heifers are left out: they have no lactation to end.
func (b *ListBuilder) DryOff(e env.Env) ([]Row, error) {
	return b.pick(e, func(s subject, row *Row) bool {
		row.Due = b.Lactations.DueDryOff(e, s.calving)
		return s.served && s.a.IsCow() && !s.l.Dry() &&
			!e.Today().Before(row.Due.AddDate(0, 0, -e.Settings.DryOffNoticeDays))
	})
}

// Calving lists every cow and in-calf heifer due to calve within three weeks,
// soonest first, and marks the cows heading for a short dry period.
func (b *ListBuilder) Calving(e env.Env) ([]Row, error) {
	return b.pick(e, func(s subject, row *Row) bool {
		row.Due, row.Note = s.calving, s.in.Sire
		if s.l.Dry() && int(s.calving.Sub(*s.l.DriedOff).Hours()/24) < lactation.ShortDryPeriodDays {
			row.Note += ", short dry period"
		}
		return s.served && !s.calving.Before(e.Today()) && !s.calving.After(e.Today().AddDate(0, 0, 21))
	})
}

// Serve lists the cows past their VWP and not served since calving, the cows served
// over 24 days ago and not confirmed in calf, and maiden heifers of 13 months and more.
func (b *ListBuilder) Serve(e env.Env) ([]Row, error) {
	return b.pick(e, func(s subject, row *Row) bool {
		row.Due = s.in.On
		if s.served {
			return !s.in.Confirmed && e.Today().Sub(s.in.On) > 24*24*time.Hour
		}
		return s.a.IsHeifer() && s.a.AgeMonths(e.Today()) >= 13 || s.a.IsCow() && b.Lactations.PastVWP(e, s.l)
	})
}

// Cull lists the animals marked to leave the herd, noting any open meat withdrawal.
func (b *ListBuilder) Cull(e env.Env) ([]Row, error) {
	open, err := b.Treatments.Open(e)
	if err != nil {
		return nil, err
	}
	return b.pick(e, func(s subject, row *Row) bool {
		for _, w := range open[s.a.Tag] {
			if w.Kind == treatment.MeatWithdrawal {
				row.Due, row.Note = w.Ends, "not saleable until "+w.Ends.Format(time.DateOnly)
			}
		}
		return s.a.CullMarked
	})
}

type subject struct {
	a       herd.Animal
	l       lactation.Lactation
	in      lactation.Insemination
	served  bool
	calving time.Time
}

// pick walks the herd, lets keep fill in a row for each animal, and returns the rows it kept.
func (b *ListBuilder) pick(e env.Env, keep func(subject, *Row) bool) ([]Row, error) {
	animals, err := b.Herd.InHerd(e)
	if err != nil {
		return nil, err
	}
	rows := []Row{}
	for _, a := range animals {
		s := subject{a: a}
		if s.l, _, err = b.Lactations.Current(e, a.Tag); err != nil {
			return nil, err
		}
		if s.in, s.served, err = b.Lactations.LastService(e, a.Tag); err != nil {
			return nil, err
		}
		s.calving = b.Lactations.ExpectedCalving(e, s.in)
		row := Row{Animal: a, DIM: s.l.DaysInMilk(e.Today())}
		if keep(s, &row) {
			rows = append(rows, row)
		}
	}
	sort.Slice(rows, func(i, j int) bool { return rows[i].Due.Before(rows[j].Due) })
	return rows, nil
}
