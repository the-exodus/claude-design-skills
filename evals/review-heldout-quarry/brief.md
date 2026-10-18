# Postpone a planned blast

## Why

Blasts are often stood down on the day: wind blowing towards the village, a
misfire check on the previous shot running long, a neighbour asking for an
hour's grace. Today the shotfirer has to cancel the blast and add it again.
That gives the blast a new id, loses the link to the notice the neighbours
already hold, and leaves the blast log full of cancel/re-add pairs that the
planning officer has to puzzle out.

## Behaviour wanted

A `postpone` command (`blastplan postpone <blast-id> [--to "YYYY-MM-DD HH:MM"]`)
and the matching library call, which move a planned blast to a later time.

## Acceptance criteria

1. Postponing moves a planned blast to a new time and keeps its id, bench,
   charge and distance. The new time must be later than the blast's current
   time.
2. The new time must pass the same rules as a newly planned blast: inside the
   permitted window in site local time, and at least `min_interval_minutes`
   from every other planned blast.
3. If no time is given, the blast moves to the earliest time that satisfies
   criterion 2 and is at least `notice_hours` after now.
4. Every receptor that received the original notice gets a revised notice,
   which replaces the original notice file in the outbox, gives the new time
   and says it replaces the earlier notice. The new time must be at least
   `notice_hours` after the revised notice is issued.
5. A blast can be postponed at most `max_postponements` times (a new setting,
   default 2). After that, postponing is refused with a message telling the
   shotfirer to cancel the blast and plan a new one.
6. Postponing does not repeat the vibration check: the charge and distance do
   not change, and the prediction does not depend on the time of day.

## Edge cases

- Cancelled and fired blasts cannot be postponed.
- The blast's own current slot does not count as a clash for its new time.
- If no notice has been issued for the blast yet, postponing issues none;
  the usual `notify` step covers it.
- The revised notice goes to the receptors who were told about the blast,
  whoever they are now: a receptor removed from the configuration since the
  original notice still gets one, and a receptor added since does not (they
  were never told of the blast and will get notices for future blasts).
