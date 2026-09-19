// Command byre runs the herd management service for one dairy farm.
//
//	byre -config byre.yaml serve    take the meter feed and serve the pages
//	byre -config byre.yaml lists    print today's lists and exit
package main

import (
	"database/sql"
	"encoding/json"
	"flag"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"path/filepath"
	"time"

	_ "github.com/mattn/go-sqlite3"

	"holmdairy.example/byre/internal/env"
	"holmdairy.example/byre/internal/herd"
	"holmdairy.example/byre/internal/lactation"
	"holmdairy.example/byre/internal/lists"
	"holmdairy.example/byre/internal/milking"
	"holmdairy.example/byre/internal/treatment"
)

// wallClock is the clock the running program uses.
type wallClock struct{}

func (wallClock) Now() time.Time { return time.Now() }

func main() {
	config := flag.String("config", "byre.yaml", "path to the farm's settings")
	flag.Parse()
	log := slog.New(slog.NewTextHandler(os.Stderr, nil))

	settings, err := env.Load(*config)
	if err != nil {
		log.Error("cannot start", "err", err)
		os.Exit(1)
	}
	db, err := sql.Open("sqlite3", filepath.Join(filepath.Dir(*config), "byre.db"))
	if err != nil {
		log.Error("cannot open the herd records", "err", err)
		os.Exit(1)
	}
	defer db.Close()
	e := env.Env{Settings: settings, Clock: wallClock{}, DB: db, Log: log}

	store := herd.NewHerdStore()
	treatments := &treatment.TreatmentService{}
	builder := &lists.ListBuilder{
		Herd:       store,
		Lactations: lactation.NewLactationService(store),
		Treatments: treatments,
	}
	if err := treatments.OpenSession(e); err != nil {
		log.Error("cannot read the open withdrawals", "err", err)
		os.Exit(1)
	}

	switch flag.Arg(0) {
	case "lists":
		printLists(e, builder)
	case "serve":
		serve(e, treatments)
	default:
		fmt.Fprintln(os.Stderr, "usage: byre -config byre.yaml serve|lists")
		os.Exit(2)
	}
}

// printLists writes today's lists to standard output, in the order the herd
// manager reads them before the morning session.
func printLists(e env.Env, b *lists.ListBuilder) {
	for _, l := range []struct {
		title string
		build func(env.Env) ([]lists.Row, error)
	}{
		{"Withhold", b.Withhold}, {"Dry-off", b.DryOff}, {"Calving", b.Calving}, {"Serve", b.Serve}, {"Cull", b.Cull},
	} {
		rows, err := l.build(e)
		if err != nil {
			e.Log.Error("list failed", "list", l.title, "err", err)
			continue
		}
		fmt.Printf("%s: %s, %s\n", e.Settings.HerdName, l.title, e.Today().Format(time.DateOnly))
		for _, r := range rows {
			fmt.Printf("  %-14s %-12s %-9s parity %d  DIM %3d  %s  %s\n", r.Animal.Tag, r.Animal.Name,
				r.Animal.Group, r.Animal.Parity, r.DIM, r.Due.Format(time.DateOnly), r.Note)
		}
	}
}

// serve takes readings from the parlour on /meter and answers until stopped.
// The withhold list is brought up to date as each session opens.
func serve(e env.Env, t *treatment.TreatmentService) {
	ingest := &milking.MeterIngest{
		Withheld: t.Withheld,
		OnSessionOpen: func(e env.Env, s milking.Session) {
			if err := t.OpenSession(e); err != nil {
				e.Log.Error("withhold list not rebuilt", "slot", s.Slot, "err", err)
			}
		},
	}
	http.HandleFunc("/meter", func(w http.ResponseWriter, r *http.Request) {
		var reading milking.Reading
		if err := json.NewDecoder(r.Body).Decode(&reading); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		if _, err := ingest.Accept(e, reading); err != nil {
			http.Error(w, err.Error(), http.StatusUnprocessableEntity)
		}
	})
	e.Log.Info("byre is up", "herd", e.Settings.HerdName, "addr", ":8420")
	e.Log.Error("stopped", "err", http.ListenAndServe(":8420", nil))
}
