package herd

import (
	"database/sql"
	"errors"
	"fmt"

	"holmdairy.example/byre/internal/env"
)

// ErrNoAnimal is returned when no animal carries the ear tag asked for.
var ErrNoAnimal = errors.New("no animal with that ear tag")

// HerdStore reads and writes animal records. Every other package goes
// through it; none of them touches the animals table.
type HerdStore struct{}

// NewHerdStore returns the store. It holds nothing itself: the database
// handle arrives with each call.
func NewHerdStore() *HerdStore {
	return &HerdStore{}
}

const animalColumns = `tag, name, sex, born, parity, grp, cull_marked, left_on`

// Get returns the animal with the given ear tag, or ErrNoAnimal.
func (s *HerdStore) Get(e env.Env, tag string) (Animal, error) {
	row := e.DB.QueryRow(`SELECT `+animalColumns+` FROM animals WHERE tag = ?`, tag)
	a, err := scanAnimal(row)
	if errors.Is(err, sql.ErrNoRows) {
		return Animal{}, fmt.Errorf("%s: %w", tag, ErrNoAnimal)
	}
	return a, err
}

// Put writes a, replacing any record already held under her ear tag.
func (s *HerdStore) Put(e env.Env, a Animal) error {
	_, err := e.DB.Exec(
		`INSERT OR REPLACE INTO animals (`+animalColumns+`) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
		a.Tag, a.Name, string(a.Sex), a.Born, a.Parity, a.Group, a.CullMarked, a.Left,
	)
	if err != nil {
		return fmt.Errorf("save %s: %w", a.Tag, err)
	}
	return nil
}

// InHerd returns every animal that has not left the herd, in ear tag order.
func (s *HerdStore) InHerd(e env.Env) ([]Animal, error) {
	rows, err := e.DB.Query(`SELECT ` + animalColumns + ` FROM animals WHERE left_on IS NULL ORDER BY tag`)
	if err != nil {
		return nil, fmt.Errorf("list herd: %w", err)
	}
	defer rows.Close()

	var herd []Animal
	for rows.Next() {
		a, err := scanAnimal(rows)
		if err != nil {
			return nil, err
		}
		herd = append(herd, a)
	}
	return herd, rows.Err()
}

// scanner is the part of *sql.Row and *sql.Rows that scanAnimal needs.
type scanner interface {
	Scan(dest ...any) error
}

func scanAnimal(sc scanner) (Animal, error) {
	var a Animal
	var sex string
	var left sql.NullTime
	if err := sc.Scan(&a.Tag, &a.Name, &sex, &a.Born, &a.Parity, &a.Group, &a.CullMarked, &left); err != nil {
		return Animal{}, err
	}
	a.Sex = Sex(sex)
	if left.Valid {
		a.Left = &left.Time
	}
	return a, nil
}
