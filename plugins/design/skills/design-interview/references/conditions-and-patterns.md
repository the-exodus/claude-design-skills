# Design Interview Reference

Two catalogues for the `design-interview` skill, used at two different moments.

**Conditions of the work** are properties a design can have. Each one that holds implies branches the universal core doesn't cover. Checked when the tree is seeded, and re-checked as it grows.

**Ambiguity patterns** are recurring shapes of under-specification that a design can carry all the way into implementation without anyone noticing. Matched against a branch while it's being interrogated.

Neither is a coverage checklist. Generic questions — "what's the auth model", "what's the expected load", "which fields are required" — you will ask anyway, and asking them from a list produces exactly the vague probes the skill is supposed to avoid. Everything here earns its place by a harder test: **a competent engineer can plausibly miss it entirely.**

**How to use.** This file has two entry points, used at two different moments.

- **At seeding** (skill Phase 4), read *Conditions of the work* below. Check each condition against the design and seed the branches that the ones holding imply. This is how the tree gets branches the pitch never gestured at.
- **During a branch interview** (Phase 5), read *Ambiguity patterns*. Match patterns to the shape of the branch in front of you — usually one to three apply, sometimes none — and read only those sections.

Re-check the conditions as the tree grows. A branch closing in Phase 5 regularly reveals a condition that wasn't visible from the pitch.

**The examples are illustrations, not questions.** They are drawn from deliberately unrelated domains so that nothing here reads as belonging to any one kind of software. Translate into the design at hand. Asking an example verbatim is a failure mode — it produces a question about someone else's system.

# Conditions of the work

Software design principles don't vary by what kind of software you're building, and neither does this list. What varies is which *properties* the work has. Each condition below, when it holds, implies branches that the universal core doesn't cover.

Check every condition. They compose freely and most non-trivial work matches several. A condition that doesn't hold costs one line of thought; a condition that holds and goes unnoticed costs a branch that never got opened.

Do not classify the work in order to use this list. "This is a CLI" is not a step — the question is whether a person waits on it, whether its config outlives a release, whether anything else calls it. Categories collapse; properties don't.

## A person waits on it

Someone is blocked while this runs. Seed: perceived latency and what fills the wait, progress and feedback, whether it can be cancelled and what a cancel leaves behind, how an error is presented and what the person does next, what "still working" looks like versus "hung".

## It runs unattended

It can fail with nobody present. Seed: recovery without intervention, what state a crash mid-operation leaves behind, safe restart and resumption, where a failure gets recorded so it's findable later, what happens when the failure is silent.

## Someone operates it in production

There is a person responsible for it who needs instruments. Seed: what signal says it's unhealthy and whether it's collected, what a diagnosis actually needs at incident time, deploy and rollback path, what's worth waking someone for and what isn't.

## Callers you can't change in lockstep

Something depends on this that ships on its own schedule — other services, other teams, installed clients, downstream libraries, plugins. Seed: interface stability guarantees, versioning and evolution path, deprecation and removal path, behavior when old and new meet, whether a compat window exists and how long it lasts, who ships first.

## State outlives a single version

Anything written by one version and read by another: stored data, files on disk, caches, serialized state, config, message formats. Seed: forward and backward compatibility, migration path, what a rollback does to data the new version already migrated, how the version of an artifact is discovered.

## The same concept has more than one shape

A concept exists in more than one representation: an in-memory type, a serialized payload, a stored record, a wire or API resource, a config object. Seed: which shapes exist and which one is authoritative, where the mapping between them lives and whether it's lossy, whether changing one forces changes to the others, where each invariant is actually enforced, whether identity survives a round trip, and which shapes are versioned independently of each other.

## It changes something already in use

Not greenfield. Seed: blast radius, migration path for existing state and callers, what "done" means for the old path, deprecation and removal sequencing, rollout ordering and flagging, how to tell whether anything still depends on the old behavior.

## More than one actor touches the same thing

Concurrent writers, parallel workers, multiple sessions, retries racing the original. Seed: what's ordered and what isn't, conflict detection versus silent resolution, locking or serialization strategy, what a loser sees.

## Work is deferred, queued, or retried

Anything that doesn't complete inline. Seed: idempotency and at what granularity, replay and reprocessing, what happens to work that fails repeatedly, backpressure when producers outrun consumers, entities that can sit unfinished forever.

## Untrusted input crosses in

Input from outside the trust boundary: user input, files, network payloads, plugins, deserialized data, anything an attacker can shape. Seed: where validation happens and whether every entry path has it, where authorization is decided and whether it has enough context, what a refusal discloses, audit trail for privileged paths.

## It runs inside a constrained envelope

Bounded memory, storage, power, bandwidth, time, or process lifetime — embedded targets, browsers, mobile, CI runners, serverless, anything with a hard ceiling. Seed: the budget and who enforces it, behavior as the limit is approached versus crossed, what degrades first and whether that's a choice or an accident.

## Behavior is learned rather than specified

Model output, heuristics, ranking, anything where correctness is statistical. Seed: evaluation criteria and baseline, data provenance, reproducibility, drift and when to revisit, behavior on out-of-distribution input, how a wrong-but-confident output is caught.

## It holds data that belongs to someone else

User data, customer data, regulated data. Seed: retention and deletion, who can see what, export and portability, what deletion means for derived copies and backups, jurisdiction if relevant.

# Ambiguity patterns

These apply during a branch interview, not at seeding.

## Directionality

When A relates to B — grants, depends on, follows, blocks, references, delegates to — B's relation back to A is a separate question with a separate answer. Resolve each direction independently. The asymmetry is usually intended and almost never stated.

Probe:
- Does the reverse relation exist at all? Is it automatic, or does it require its own action?
- Does the reverse carry the same rights and effects, or weaker ones?
- Can the two directions disagree, and what does the system do when they do?
- Who can observe the relation — A, B, both, third parties?

Examples:
- A user blocks another: does the blocked user's view change, or only the blocker's?
- Service A declares a dependency on B: does B know it has a dependent, and does that constrain B's deploys?
- A task spawns a subtask: does cancelling the parent cancel the child? Does a failed child fail the parent?
- A document links to another: is there a backlink? Does deleting the target break the source, rewrite it, or leave it dangling?

## Expiry and stuck states

Any state that isn't terminal is a state something can sit in forever: pending, in-flight, held, reserved, partially applied.

Probe:
- Which states are non-terminal? What moves an entity out of each?
- If nobody acts, does it expire? After how long, measured from what event?
- Who can force-resolve a stuck entity, and through what interface?
- Is there a sweeper, or is human action the only exit?
- What does a stuck entity look like to whoever encounters it — visibly stuck, or indistinguishable from normal?

Examples:
- A lock or lease whose holder died without releasing it
- A migration that failed midway, leaving rows in an intermediate schema
- A job dequeued by a worker that was killed before acking
- A temp file written but never renamed into place
- An invite, approval, or handshake nobody ever acted on

## Reversal semantics

Undo is rarely the inverse of do. The original action produced derived state — notifications, caches, audit records, downstream copies, files on disk — and each piece needs its own answer: reverted, kept, or marked revoked.

Probe:
- What exactly does the reversal touch, and what does it deliberately leave behind?
- Are history and audit entries removed, or is the reversal itself an entry?
- Does reversal cascade to dependents, or is it surgical and leaves them dangling?
- Is there a time bound past which reversal is refused? What does a late request get?
- Does anyone who learned about the original action learn about the reversal?

Examples:
- Uninstall: config, user data, generated caches — which survive, and who decides?
- A rollback where the new version already wrote data the old version can't read
- Revoking a credential that has already been used to mint downstream tokens
- Deleting a record that other records reference
- `git revert` versus `git reset`: compensating entry or erasure is the choice being made

## Rule precedence

When several independent rules bear on the same decision, the order matters, and it usually exists only in someone's head.

Probe:
- Enumerate every rule that can apply to this decision. Which wins?
- Is precedence fixed, or value-dependent? ("Most restrictive wins" is a legitimate rule — name it as one.)
- Can two rules deadlock, each blocking the other's resolution?
- Where does a caller learn *which* rule applied, as opposed to just the outcome?

Examples:
- CLI flag vs. environment variable vs. config file vs. compiled default
- A deny rule and an allow rule both matching the same request
- Per-user, per-key, and global limits on a single call
- A user preference contradicted by a safety or regulatory requirement
- Two sources defining the same key, and the merge strategy nobody wrote down

## Identity and equality

What makes two things the same thing? Nearly every system has a dedup, lookup, or already-did-this path, and the notion of equality it relies on is rarely stated.

Probe:
- What is identity here — a field, a derivation, a location? Is it stable for the entity's whole life?
- Is identity assigned by us or supplied by the caller? If supplied, what happens on collision?
- Is comparison exact, case-insensitive, trimmed, normalized? Under whose normalization?
- Can identity change? What happens to existing references when it does?
- Does content-identity or location-identity govern — and does the answer differ per operation?

Examples:
- Two paths reaching the same file through a symlink or bind mount
- Names differing only by Unicode normalization form, or by homoglyph
- A retry carrying the same idempotency key but a different payload
- A package version republished with different contents under the same version string
- Case-insensitive filesystem beneath case-sensitive application logic

## Cardinality and bounds

Designs get described in the plural-and-typical case. Zero, exactly one, and very many each behave differently, and unbounded is a decision rather than a default.

Probe:
- What happens at zero — empty result, error, or a special-cased default?
- Is exactly-one special? Is that enforced, or merely assumed?
- Is there a maximum? Who enforces it, and what does hitting it look like to the caller?
- If unbounded, what grows without limit, and does anything ever reclaim it?
- Does the shape of the operation change at large N — batching, pagination, streaming — and is that visible in the interface, or a surprise?

Examples:
- A listing that must render, sort, or diff a million entries
- A config field documented as a single value that someone eventually needs twice
- An append-only path with no retention story
- An argument list that exceeds the OS limit
- A fan-out whose size is the product of two collections

## Time

Time enters as a hidden input almost everywhere and is treated as one almost nowhere.

Probe:
- Which clock: wall or monotonic? What breaks if wall time steps backward?
- Is a stored time an instant, a local time, or a date? In what zone, and whose?
- Is this a deadline or a duration? Where does one become the other?
- What clock skew is tolerated between the machine that writes and the machine that reads?
- Is "now" injectable, or is behavior at time boundaries untestable?
- What happens at a DST transition, or when a date-only field crosses midnight in some other zone?

Examples:
- A timeout computed from wall time across an NTP correction
- Work scheduled in local time in a region that changes its offset
- A token whose issuer and verifier disagree about expiry by a few seconds
- Records ordered by timestamp where two writers' clocks disagree
- A "days until" computation that gives different answers to different readers

## Ordering and concurrency

What is guaranteed to happen in order, and what two simultaneous actors do to each other.

Probe:
- Is ordering guaranteed anywhere here? By what mechanism, over what scope — globally, per key, per session?
- Can two actors do this at once? What's the outcome — last write wins, merge, reject, serialize?
- Is a conflict detected or silently resolved? If detected, what does the loser see?
- Are there operations that are safe alone but unsafe interleaved?
- Does the design assume a single writer anywhere without enforcing it?

Examples:
- Two processes writing the same file with no lock
- Read-modify-write on a counter under concurrent requests
- Out-of-order delivery in a stream partitioned by a key that isn't the ordering key
- Two sessions or agents editing the same working tree
- A cache populated by one request while another invalidates it

## Atomicity and partial failure

Any operation with more than one effect can stop between them.

Probe:
- List this operation's effects. Which are atomic with which? Where are the seams?
- Fail it at each seam in turn: what state is left behind, and is that a state the rest of the design knows about?
- Which effects are durable and which are best-effort? Is that stated, or assumed?
- Is retry safe after a partial failure? At what granularity is it idempotent — request, effect, both?
- Does anything clean up after a partial failure, or does it need a human?

Examples:
- A write plus a notification where the notification lands and the write rolls back
- An installer that unpacks files, edits a system config, and registers a service
- A change spanning several repositories or several services
- A file rewritten in place and interrupted midway
- A batch where item 400 of 1000 fails

## Evolution and compatibility

Old things meet new code. Not just APIs — anything persisted or produced by one version and consumed by another.

Probe:
- What outlives a single version here: stored data, files, caches, serialized state, config, plugin interfaces, message formats?
- Can new code read what old code wrote? Can old code read what new code wrote — and does it need to, for rollback, a mixed fleet, or a staged rollout?
- What does an unknown field, value, or version do: reject, ignore, or preserve and pass through?
- Is the version discoverable from the artifact itself, or inferred from context?
- What's the removal path for something deprecated? How does a straggler find out?

Examples:
- A cache serialized by one release and read by the next
- A config file that gains a required key
- A saved document or project file opened by an older build
- A rollback after the new version already migrated the schema
- A plugin compiled against the previous interface

## Trust boundaries

Where untrusted things enter, and where the check that they're allowed actually happens.

Probe:
- Draw the boundary: what's inside, what's outside, what crosses?
- Enumerate every path in. Is the check on each path, or only the obvious one? What about the batch path, the CLI, the admin path, the import or replay path?
- Is authorization checked at the layer with enough context to decide, or somewhere upstream that's guessing?
- Is validation done once at entry, or repeated at each layer that assumes it already happened?
- What does a refusal disclose? Does the shape of the failure reveal the existence of something?
- Are there bypass paths for operators or automation? Are those recorded?

Examples:
- A parser handed a file from an untrusted source
- A plugin or extension running inside the host's process
- Deserialization that can construct arbitrary types
- A background job reprocessing input that was validated under since-changed rules
- A name or path from input used to build a filesystem location

## Failure surfacing

Something has gone wrong. Who finds out, through what channel, and can they act on it?

Probe:
- For each failure mode: who needs to know — the caller, the end user, an operator, nobody?
- What's the channel for each audience: return value, exit code, stderr, log line, metric, alert, UI state?
- Does the message say what to do, or only what happened?
- Is a failure nobody is watching distinguishable from success? Where are the silent-failure paths?
- Is there something a person would want to know that's currently knowable only by reading the code?
- For degradation rather than failure: is it visible, or does it just look slow?

Examples:
- A library that swallows an error and returns a zero value
- A CLI that exits 0 after a step failed
- A retry loop that eventually succeeds and hides that four attempts didn't
- A fallback so effective that nobody notices the primary is down
- A partial result rendered identically to a complete one
