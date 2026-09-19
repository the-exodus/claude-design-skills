// Package herd keeps the record of every animal on the farm and the
// management group each one is in.
package herd

import "time"

// Sex is the sex of an animal as registered at birth.
type Sex string

const (
	Female Sex = "F"
	Male   Sex = "M"
)

// Animal is the record of one animal, from birth or purchase until she
// leaves the herd.
type Animal struct {
	// Tag is the ear tag, exactly as printed. It is the animal's identity.
	Tag  string
	Name string
	Sex  Sex
	Born time.Time

	// Parity is the number of times she has calved (glossary: parity).
	Parity int

	// Group is the name of the management group she is in today.
	Group string

	// CullMarked is set when the herd manager has decided she is to leave
	// the herd. She stays in the herd, and on the cull list, until Left is set.
	CullMarked bool

	// Left is the day she left the herd, sold or dead. Nil while she is here.
	Left *time.Time
}

// IsHeifer reports whether a is a heifer: a female that has not yet calved.
func (a Animal) IsHeifer() bool {
	return a.Sex == Female && a.Parity == 0
}

// IsCow reports whether a is a cow: a female that has calved at least once.
func (a Animal) IsCow() bool {
	return a.Sex == Female && a.Parity > 0
}

// InHerd reports whether a is still on the farm.
func (a Animal) InHerd() bool {
	return a.Left == nil
}

// AgeMonths returns a's age in whole months on the given day.
func (a Animal) AgeMonths(on time.Time) int {
	months := (on.Year()-a.Born.Year())*12 + int(on.Month()) - int(a.Born.Month())
	if on.Day() < a.Born.Day() {
		months--
	}
	return months
}
