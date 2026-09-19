package herd

import (
	"fmt"
	"slices"
	"time"

	"holmdairy.example/byre/internal/env"
)

// The groups Byre itself suggests moves into. A farm may define others, but
// these three names must be among its groups.
const (
	GroupMilkers = "milkers"
	GroupDry     = "dry"
	GroupCloseUp = "close-up"
)

// Move is one change of management group, kept so that the history of where
// an animal has been can be read back.
type Move struct {
	Tag    string
	From   string
	To     string
	On     time.Time
	Reason string
}

// GroupManager moves animals between management groups and suggests the
// moves that follow a dry off, the close-up window and a calving.
type GroupManager struct {
	store *HerdStore
}

// NewGroupManager returns a manager that moves animals held in store.
func NewGroupManager(store *HerdStore) *GroupManager {
	return &GroupManager{store: store}
}

// MoveTo puts the animal in the named group and records the move. An animal
// is only ever in one group, so the move out of the old one is implied.
func (g *GroupManager) MoveTo(e env.Env, tag, group, reason string) (Move, error) {
	if !slices.Contains(e.Settings.Groups, group) {
		return Move{}, fmt.Errorf("move %s: %q is not one of the farm's groups", tag, group)
	}
	a, err := g.store.Get(e, tag)
	if err != nil {
		return Move{}, err
	}
	m := Move{Tag: tag, From: a.Group, To: group, On: e.Today(), Reason: reason}
	a.Group = group
	if err := g.store.Put(e, a); err != nil {
		return Move{}, err
	}
	_, err = e.DB.Exec(`INSERT INTO moves (tag, from_grp, to_grp, on_day, reason) VALUES (?, ?, ?, ?, ?)`,
		m.Tag, m.From, m.To, m.On, m.Reason)
	if err != nil {
		return Move{}, fmt.Errorf("record move of %s: %w", tag, err)
	}
	return m, nil
}

// Suggest returns the group the animal ought to be in, given whether she is
// dry and when she is expected to calve, and whether that differs from where
// she is. The herd manager confirms a suggestion; Byre never moves an animal
// on its own.
func (g *GroupManager) Suggest(e env.Env, a Animal, dry bool, expectedCalving *time.Time) (string, bool) {
	want := a.Group
	switch {
	case expectedCalving != nil && (dry || a.IsHeifer()) &&
		!e.Today().Before(expectedCalving.AddDate(0, 0, -e.Settings.CloseUpDays)):
		want = GroupCloseUp
	case dry:
		want = GroupDry
	case a.IsCow():
		want = GroupMilkers
	}
	return want, want != a.Group
}
