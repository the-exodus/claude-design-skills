Written to `docs/lexicon.md` — 22 entries → 13. Everything below is the report.

## Verdicts

**Kept as they were (2)** — pass all three tests, already in shape.

| Entry | Reason |
|---|---|
| `send` | Meaning plus the distinction from *move*, nothing else; matches `WorkspaceManager.cs:81-94`. |
| `work area` | Narrower than "screen", and the second sentence is the distinction that earns the entry. |

**Rewrote (8)** — term passes, entry carried code or behaviour.

| Entry | Reason |
|---|---|
| `floating window` | Dropped "The `WorkspaceManager` tracks it like any other window" (names a class); added the distinction from *unmanaged window*, which is why the entry exists. |
| `layout` | 150 words of engine, pure-function consequence, default history and per-layout behaviour cut to the meaning; the term itself is fine. |
| `main tile` | Dropped "Its width is set by the *split ratio*" — *split ratio* already says it from the other side. |
| `move` | Named *send* explicitly, so each of the pair points at the other. |
| `rule` | Kept the definition; cut the "applied only once" sentence (drift D1) and added the ADR 0003 pointer. |
| `shortcut` | Passes test 2 only because of the Windows `.lnk` overload, which the entry never stated. Now it does. |
| `split ratio` | Cut the grow/shrink commands (`configuration.md:51,69`) — verbs and their arguments are the reference's. |
| `workspace` | Cut "its own *layout* and *split ratio*" (each of those entries carries its half) and stated the virtual-desktop overload that makes the word need defining. |

**Merged (1)**

| Entry | Into | Reason |
|---|---|---|
| `pane` | `tile` | Same definition, word for word. `pane` appears nowhere in the code or docs; recorded in *tile* as not used. |

**Renamed (1)**

| Entry | To | Reason |
|---|---|---|
| `zoom` | `promote` | Test 3: the headword appears in no source. Every source says promote — `configuration.md:18,58,68`, `README.md:9`, `Workspace.cs:110`, `HotkeyListener.cs:83`. `zoom` recorded as not used. **Awaits your sign-off** (listed again under decisions). |

**Rewrote from a redirect (1)**

| Entry | Reason |
|---|---|
| `unmanaged window` | Was "See *floating window*". It passes tests 1 and 2 and is not a synonym — it is the near-synonym the whole distinction hangs on. Now a distinct entry. See drift D2. |

**Retired (9)**

| Entry | Test | Reason / where the word belongs |
|---|---|---|
| `click-to-focus policy` | 2 | Standard window-manager phrase used in its ordinary sense; its only specific content is a decision → ADR 0002. The headword appears in no source. |
| `config file` | 2 | Ordinary sense throughout. → `configuration.md:3`. |
| `context` | 1 | Names the `WmContext` class, down to "Written `ctx` in code". → the type and `conventions.md:15`. |
| `HotkeyListener` | 1 | A class. The concept users meet is *shortcut*, which survives. |
| `LayoutEngine` | 1 | A class. |
| `orphan sweep` | 1 | Names a routine (`WorkspaceManager.SweepOrphans`). The guarantee it serves is stated plainly in `README.md:12` and needs no word of its own — see the decision list if you disagree. |
| `RuleEngine` | 1 | A class. The concept is *rule*. |
| `WorkspaceManager` | 1 | A class. |
| `unmanaged window` (as redirect) | — | Superseded by the rewrite above, not a retirement. |

That is 8 real retirements plus the redirect. Retiring under test 2 (`config file`, `click-to-focus policy`) does not ban the words — they are ordinary and free to use.

## Where the cut content already lives

- `layout`'s engine sentence → `adr/0001-layouts-are-pure-functions.md:13`, `LayoutEngine.cs:8-11,38-60`.
- `layout`'s "cannot remember sizes / dragging has no lasting effect" → `adr/0001:20`, verbatim.
- `layout`'s main-stack/columns descriptions and `default_layout` → `configuration.md:49,56`, `MainStackLayout.cs:6-9`, `ColumnsLayout.cs:6-9`.
- `click-to-focus policy` → `adr/0002:13` (decision), `:9,17` (rationale), `configuration.md:76`, `README.md:9`.
- `config file` → `configuration.md:3`, `README.md:17-18`.
- `context` → `WmContext.cs:38-44`, `conventions.md:15`.
- `HotkeyListener` → `HotkeyListener.cs:16-20,27-40`, `configuration.md:60-62`.
- `LayoutEngine` → `LayoutEngine.cs:8-12,38`.
- `orphan sweep` → `configuration.md:105`, `README.md:12`, `WorkspaceManager.cs:96-115` (all three say *same-numbered* workspaces, which the entry omitted).
- `RuleEngine` → `RuleEngine.cs:9-26`, `configuration.md:80`.
- `WorkspaceManager` → `WorkspaceManager.cs:8-9`.
- `split ratio`'s grow/shrink sentence → `configuration.md:51,69`, `TesseraConfig.cs:31`, `HotkeyListener.cs:86-89`.
- `tile`'s "cover the *work area* apart from the gutters" → `ILayout.cs:35-39`, `configuration.md:52`.
- `floating window`'s `WorkspaceManager` sentence → `WorkspaceManager.cs:52,62,65`, `LayoutEngine.cs:55-57`.
- `main tile`'s width sentence → `configuration.md:50`, and the surviving *split ratio* entry.

## Homeless content — two items

- From *layout*: "When a workspace holds a single window, every layout gives it the whole work area." Stated nowhere outside the lexicon.

> "The default was columns until 0.4; it became main-stack because on ultrawide monitors equal columns pushed the editor off-centre." (was `lexicon.md:21`)

Nowhere else. `TesseraConfig.cs:24-25` points at it without carrying it — "This default has history; ask before changing it" — and `configuration.md:49` gives the default with no reason. **This is a missing decision record.** I have not written it; the sentence above is the whole of what was lost, preserved here so you can lift it into `adr/0004`.

## Drift — the lexicon against the code and docs

**D1 — a rule is not applied only once.** `lexicon.md:33` said "A rule is applied only once, when the window first opens; nothing that happens to the window afterwards ever triggers a rule again." Contradicted by `adr/0003-rules-reapplied-on-title-change.md:13` ("`on = "title"` applies the rule whenever the title of a managed window changes"), `configuration.md:87`, `Rule.cs:9-10`, `RuleEngine.cs:33-37`. The claim is behaviour, so it is not carried into the new entry — the lexicon simply no longer asserts it. Nothing to decide unless you think ADR 0003 is the stale side.

**D2 — unmanaged is not floating.** `lexicon.md:45` said "**unmanaged window** — See *floating window*." Contradicted by `configuration.md:95` ("`float` and `ignore` are not the same thing"), `configuration.md:97-99`, `Rule.cs:19-23`, `WmContext.cs:73-77`, `adr/0003:18-19`. Four sources agree against the lexicon, so I wrote the distinct entry from them.

**D3 — the split ratio is not quite the share of the width.** `lexicon.md:41` and `configuration.md:50` both say "the share of the *work area*'s width given to the *main tile*". `MainStackLayout.cs:25` computes `round(area.Width * SplitRatio) - input.Gutter / 2`, and `MainStackLayout.cs:9` says so: "less half a gutter". The two docs agree with each other and the code differs by half a gutter. I kept the docs' wording unchanged. **Your call:** is the ratio the share before the gutter is taken out (docs right, code comment is the fine print) or after?

**D4 — "focus passes to the next window" has an unstated exception.** `lexicon.md:37`, kept verbatim in *send*. `WorkspaceManager.cs:86` takes `source.Neighbour(window, 1)` before removing the window, and `Workspace.cs:86-87` returns null when the workspace has fewer than two windows — so sending the only window of a workspace leaves `ctx.Focused` null (`WorkspaceManager.cs:90`). `adr/0002:20` has the same gap. **Your call:** add the exception to the entry, or is nothing-focused simply "the next window" of an empty workspace?

**D5 — "focus changes only …" is contradicted inside its own record.** Not a surviving entry, but it is where the retired `click-to-focus policy` content lands, so it is worth knowing before you rely on it: `adr/0002:13` says "Focus changes only when the user runs a focus command or clicks a window", echoed at `configuration.md:76` and `HotkeyListener.cs:18` ("Focus only ever changes here or through a click"). But `adr/0002:20` says Tessera chooses the focus itself after `send-to-workspace` or a close, `WorkspaceManager.cs:77,90` do exactly that, and `RuleEngine.cs:48` clears the focus when a rule releases the focused window. The universal needs its exception on all three. Docs only — I changed nothing.

**D6 — minor, in retired entries.** `lexicon.md:29` re-homed windows "onto the primary monitor", omitting *same-numbered* (`configuration.md:105`, `WorkspaceManager.cs:105`). `lexicon.md:15` listed what the context carries but not the services (`WmContext.cs:39-40`). Both entries are gone; noted for completeness.

## References outside the lexicon to retired words

I changed none of these — the lexicon was the only file I touched.

- `conventions.md:8` — "When a pull request adds a class, add a lexicon entry for the class in the same pull request." This convention is what produced `HotkeyListener`, `LayoutEngine`, `RuleEngine`, `WorkspaceManager` and `context`. It contradicts test 1 and should go, or become "add a doc comment".
- `WmContext.cs:39` — `/// The context (lexicon: context) …` cites a retired word.
- `LayoutEngine.cs:9` — `/// Arranges workspaces (lexicon: LayoutEngine). …` cites a retired word.
- `configuration.md:105` — tells users about "the orphan sweep" by the routine's name. The sentence's guarantee is fine; the mechanism's name in user documentation is the drift.
- `MainStackLayout.cs:9` — `(lexicon: split ratio)` still resolves. ✅
- `conventions.md:7` cites *tile* and *send*, both surviving. ✅
- `zoom`, `pane` and `click-to-focus` appear in no file outside the lexicon, so nothing dangles from those three.

## Proposed gaps (on the file's gaps line, not admitted)

- **stack** — Every source says it (`README.md:7,9`, `configuration.md:58,66`, `adr/0001:21`, `MainStackLayout.cs:8`, `Workspace.cs:75`) and the surviving *main tile* entry uses it, but nothing defines it. It is also the textbook case of a component named to dodge a domain word: `MainStackLayout.cs:39-42` and `conventions.md:9` say `SecondaryArea` exists only because C# already owns `Stack`.
- **focused monitor** — `configuration.md:103` ("Commands act on the focused monitor, which is the monitor of the focused window") uses it in a fixed, narrower-than-ordinary sense, and `WmContext.cs:79-81` adds a case the docs never state: the primary monitor when nothing is focused.

Considered and not proposed: *gutter* (a config key — `configuration.md:52` is its home), *command* (ordinary; the fixed list is `configuration.md:64-74`), *managed window* (the complement of *unmanaged window*), *in view* (carried by *workspace*).

## Decisions for you

1. **`zoom` → `promote`.** Written under `promote` per the rename rule, since the sources are unanimous. Reversible if `zoom` is a word your users actually type.
2. **D3** — split ratio before or after the gutter.
3. **D4** — whether *send* should state the last-window case.
4. **`orphan sweep`** — I judged the guarantee needs no word, since `README.md:12` says it in plain English. If you'd rather have one, the entry would be for what the user observes (a window that is never *stranded*), not for the sweep.
5. **The virtual-desktop clause** in *workspace* is mine, from the platform rather than from your files. Drop it if it reads as noise.

## Sanity check

I ran the new lexicon through sentences someone would actually say: a bug report ("I sent a window to workspace 3 and focus went to a floating window instead of down the stack" — D4 is exactly this, which is why it is listed), a support question ("Taskmgr floats but Shell_TrayWnd is unmanaged — why can't `toggle-float` bring it back?" — answerable now that the two entries are distinct), a design question ("should a `title` rule be able to bring an unmanaged window back?"), and a review comment ("call it a tile, not a pane"). The one word that kept wanting to appear undefined was *stack*, hence the gap.
