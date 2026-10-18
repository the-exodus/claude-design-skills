# Kessler KB-30 bench scale: serial protocol (excerpt)

9600 baud, 8N1, no flow control. The scale sends one frame per reading, about
five a second, each terminated by CR LF.

## Frame format

    SS,GS,+NNNNNN.N u

| Field | Meaning |
|---|---|
| `SS` | `ST` when the reading is stable, `US` while it is settling, `OL` over capacity |
| `GS` | `GS` gross, `NT` net (after tare) |
| `+NNNNNN.N` | signed weight, one decimal |
| `u` | unit: `g` or `kg`, as set on the front panel |

Example: `ST,NT,+002400.0 g`

## Commands

| Send | Effect |
|---|---|
| `T` CR LF | tare |
| `Z` CR LF | zero |
| `P` CR LF | send one frame now |

## Power saving

After five minutes with no change on the pan the scale sleeps and stops
sending. Any change on the pan wakes it. **The first frame after waking is
always marked `ST` and repeats the last weight shown before the scale slept,
whatever is on the pan now.** Frames from the second onwards report the pan.

## Units

The unit follows the front-panel setting and can be changed by staff at any
time. Hosts that need grams must read the unit field of every frame.
