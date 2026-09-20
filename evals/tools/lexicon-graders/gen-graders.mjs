// The regex graders of the four invented lexicon fixtures, as one table.
//
//   node evals/tools/lexicon-graders/gen-graders.mjs write     rewrite evals/lexicon-*/graders/*.md
//   node evals/tools/lexicon-graders/test-graders.mjs          try every pattern on known outputs
//   node evals/tools/lexicon-graders/check-files.mjs           the files on disk match this table
//
// Run from the repository root. The table is the source of the regex graders: change a pattern
// here, test it, then write. The patterns share helpers (an entry's heading, the rest of its
// paragraph, a file:line citation, "has no home" near a sentence), which is why they are
// generated rather than kept by hand.
//
// The llm graders are NOT generated once they exist. Their rubrics are calibrated
// (evals-calibration/), and are edited by hand in the grader files; the criteria below are only
// the wording a missing file would start from. After changing a rubric, run
// evals/tools/sync-calibration-rubrics.py and re-run that grader's calibration.
//
// Never put three dashes in a row inside a grader's frontmatter, comments and patterns
// included: the runner ends the frontmatter there and the case fails to load.
import { existsSync, mkdirSync, writeFileSync } from "node:fs";

// Rest of the entry's paragraph, lazily: any char, or a newline not followed by a blank line.
const PARA = String.raw`(?:[^\n]|\n(?!\s*\n))*?`;
const H = (terms) => String.raw`^\*\*(?:${terms})\*\*`;
// A citation of `base` whose first line number is one of `lines`:
// fines.ts:6-13, `src/loans/fines.ts`:6, fines.ts (lines 6–13), fines.ts L9.
const FL = (base, lines) =>
  String.raw`${base.replace(/\./g, "\\.")}[^\n\w]{0,4}(?:lines?\s*|L)?(?:${lines})\b`;
const HOMELESS = String.raw`(?:homeless|no (?:other )?home|nowhere else|lives nowhere|not (?:recorded|stated|found) (?:anywhere|elsewhere))`;
const near = (what) =>
  String.raw`${HOMELESS}[\s\S]{0,800}?(?:${what})|(?:${what})[^\n]{0,300}?${HOMELESS}`;
const OVER_80_WORDS = String.raw`^\*\*(?:\S+(?:[ \t]+|\n(?![ \t]*\n))){80}\S`;
const NOT_REDIRECT = (term) => String.raw`^\*\*${term}\*\*(?![\s—–:-]*see\b)`;

const skillFired = {
  name: "skill-fired",
  raw: `type: tool_used\ntool: Skill\ninput_match: '"skill"\\s*:\\s*"(?:[\\w-]+:)?lexicon"'`,
};

export const cases = {
  "lexicon-shelfwise": {
    lexicon: "docs/design/lexicon.md",
    graders: [
      skillFired,
      // --- the written lexicon ---
      { name: "components-retired", why: "Test 1: component names are not entries.", file: true, absent: true, flags: "mi",
        pattern: H("CatalogIndex|FineCalculator|HoldManager|LoanReconciler|NotificationQueue|repository layer") },
      { name: "pervasive-identifier-retired", why: "Decoy: ctx is in every file, and frequency in code is not test 2.", file: true, absent: true, flags: "mi",
        pattern: String.raw`^\*\*request context` },
      { name: "ordinary-words-retired", why: "Test 2: ordinary words.", file: true, absent: true, flags: "mi", pattern: H("book|date") },
      { name: "decision-only-retired", why: "The entry only restates ADR-0004's decision.", file: true, absent: true, flags: "mi", pattern: H("patron-first policy") },
      { name: "mechanism-name-retired", why: "Mechanism vs guarantee: the routine's name is not a headword, whether the guarantee is reframed or homed elsewhere.", file: true, absent: true, flags: "mi", pattern: H("charge sweep") },
      { name: "synonym-merged", why: "Test 3: borrower is a synonym of patron.", file: true, absent: true, flags: "mi", pattern: H("borrower") },
      { name: "synonym-recorded-not-used", why: "The merge is recorded in the surviving entry.", file: true, flags: "mi", pattern: H("patron") + PARA + String.raw`\bborrower\b` },
      { name: "concept-kept-hold", guard: true, why: "Decoy: HoldManager is code, hold is the concept and stays.", file: true, flags: "mi", pattern: H("hold") },
      { name: "distinction-renew-names-extend", guard: true, why: "The distinction survives: each entry names the other. Also the Renewal DTO decoy.", file: true, flags: "mi", pattern: H("renew") + PARA + String.raw`\bextend` },
      { name: "distinction-extend-names-renew", why: "The distinction survives: each entry names the other.", file: true, flags: "mi", pattern: H("extend") + PARA + String.raw`\brenew` },
      { name: "redirect-rewritten-member", why: "Decoy: the 'See patron' stub hides a distinct concept. Kept, no longer a redirect, names patron.", file: true, flags: "mi", pattern: NOT_REDIRECT("member") + PARA + String.raw`\bpatron` },
      { name: "user-facing-term-kept", guard: true, why: "Decoy: grace period has a config key but is a word users meet.", file: true, flags: "mi", pattern: H("grace period") },
      { name: "no-code-names", why: "No component or function name anywhere in the written lexicon. Case-sensitive.", file: true, absent: true,
        pattern: String.raw`\b(?:CatalogIndex|FineCalculator|HoldManager|LoanReconciler|NotificationQueue|LoanRepository|BranchSite|OverdueState|RequestContext)\b|renew\(\)` },
      { name: "no-entry-over-80-words", why: "The bloated pickup window entry (about 140 words) is cut down; the skill's own mark is about fifty.", file: true, absent: true, flags: "m", pattern: OVER_80_WORDS },
      { name: "history-cut-from-entry", why: "The pilot sentence is history, not meaning.", file: true, absent: true, flags: "i", pattern: String.raw`2023 pilot|ten days to seven` },
      { name: "disputed-universal-not-asserted", why: "Drift: 'always accrues' is contradicted by OverdueState, so the lexicon stops asserting it.", file: true, absent: true, flags: "i", pattern: String.raw`always accrues` },
      { name: "header-admission-replaced", why: "The header's admission rule ('or a decision defined it') is replaced by the tests.", file: true, absent: true, flags: "i", pattern: String.raw`a decision defined it` },
      { name: "gap-branch-proposed", why: "The gap: BranchSite dodges the undefined domain word branch. The file has a Gaps line, so it goes there: anywhere in the header, above the horizontal rule.", file: true, flags: "mi", pattern: String.raw`^\W{0,3}Gaps\b(?:(?!\n-{3})[\s\S]){0,800}?\bbranch\b` },
      // --- the report ---
      { name: "drift-overdue-cited", why: "Drift at a known line: enum OverdueState at src/loans/fines.ts:6-13, or the uses at :26, :28, :43.", pattern: FL("fines.ts", "[5-9]|1[0-3]|26|28|43") },
      { name: "drift-receipt-cited", why: "Headword drift: due slip vs receipt, with the code cited.", pattern: FL("receipt.ts", String.raw`\d+`) },
      { name: "edge-hold-manager-cited", why: "Outside edge: (lexicon: HoldManager) at src/holds/hold-manager.ts:3.", pattern: FL("hold-manager.ts", "[1-3]") },
      { name: "edge-loan-reconciler-cited", why: "Outside edge: (lexicon: charge sweep) at src/loans/loan-reconciler.ts:2.", pattern: FL("loan-reconciler.ts", "[12]") },
      { name: "edge-configuration-cited", why: "A user reference names the mechanism: docs/configuration.md:32.", pattern: FL("configuration.md", "3[0-2]") },
      { name: "homeless-pilot-sentence", why: "The ten-to-seven-days pilot sentence has no other home and is listed as such.", flags: "i", pattern: near("pilot|ten days") },
      { name: "checkin-sentence-home", llm: true, focus: "last_message",
        criteria: `This is a report on consolidating a project lexicon. Judge one thing only: what it says about the sentence from the old "pickup window" entry, "The window starts when the item is checked in at the pickup branch, not when the patron is notified."

The written lexicon is not shown to you, only the report, so silence about this sentence is not a failure.

FAIL if the report lists that sentence, or its substance (the window starts at check-in rather than at notification), among the homeless content or as having no other home.
FAIL if the report names src/notifications/notification-queue.ts as the place where that statement lives.
PASS in every other case: the report says the statement stays in the entry, or names src/holds/hold-manager.ts as its home, or does not say where it went.` },
    ],
  },
  "lexicon-stockroom": {
    lexicon: "GLOSSARY.md",
    graders: [
      skillFired,
      { name: "components-retired", why: "Test 1: component names are not entries.", file: true, absent: true, flags: "mi",
        pattern: H("AllocationEngine|event bus|ORM session|PickListBuilder|ReservationService|SkuCache") },
      { name: "pervasive-identifier-retired", why: "Decoy: uow() is everywhere in the code, and frequency in code is not test 2.", file: true, absent: true, flags: "mi", pattern: H("unit of work") },
      { name: "ordinary-words-retired", why: "Test 2: ordinary words.", file: true, absent: true, flags: "mi", pattern: H("box|quantity") },
      { name: "decision-only-retired", why: "The phrase exists only in the glossary; the content is ADR-0004's.", file: true, absent: true, flags: "mi", pattern: H("two-phase pick") },
      { name: "mechanism-name-retired", why: "Mechanism vs guarantee: the sweep's name is not a headword, whether the guarantee is reframed or homed elsewhere.", file: true, absent: true, flags: "mi", pattern: H("reconciliation sweep") },
      { name: "unused-headword-gone", why: "No source says 'despatch note'. True whether the run renames it to packing slip or retires it.", file: true, absent: true, flags: "mi", pattern: H("despatch note") },
      { name: "synonyms-merged", why: "Test 3: item code is SKU, stock is on-hand; shelf is retired or merged into bin.", file: true, absent: true, flags: "mi", pattern: H("item code|stock|shelf") },
      { name: "synonym-recorded-not-used", why: "The merge is recorded in the surviving entry.", file: true, flags: "mi", pattern: H("SKU") + PARA + String.raw`\bitem code\b` },
      { name: "dodging-component-retired", why: "StockLot exists to dodge the domain word batch.", file: true, absent: true, flags: "mi", pattern: H("StockLot") },
      { name: "dodged-word-admitted", why: "The reframe: batch gets the entry.", file: true, flags: "mi", pattern: H("batch") },
      { name: "distinction-allocation-names-reservation", guard: true, why: "The distinction survives: each entry names the other.", file: true, flags: "mi", pattern: H("allocation") + PARA + String.raw`\breserv` },
      { name: "distinction-reservation-names-allocation", guard: true, why: "The distinction survives: each entry names the other.", file: true, flags: "mi", pattern: H("reservation") + PARA + String.raw`\ballocat` },
      { name: "distinction-stocktake-kept", guard: true, why: "The other half of the cycle count distinction. Also the CycleCount DTO decoy.", file: true, flags: "mi", pattern: H("stocktake") },
      { name: "redirect-rewritten-backorder", why: "Decoy: the 'See reservation' stub hides a distinct concept.", file: true, flags: "mi", pattern: NOT_REDIRECT("backorder") },
      { name: "exception-kept-available", guard: true, why: "Trap: without the quarantine exception, 'on-hand less reserved' is a false universal.", file: true, flags: "mi", pattern: H("available") + PARA + String.raw`quarantin` },
      { name: "user-facing-term-kept", guard: true, why: "Owner's ruling: reservation TTL has a config key but is a word operators set and say, like grace period in Shelfwise.", file: true, flags: "mi", pattern: H("reservation TTL") },
      { name: "overload-stated-pick-queue", why: "An overload that counts: the pick queue is not FIFO and not the job queue.", file: true, flags: "mi", pattern: H("pick queue") + PARA + String.raw`(?:FIFO|first[- ]in)` },
      { name: "decoy-overload-not-stated", guard: true, why: "An overload that doesn't count: nobody confuses a customer return with a return value. Passes if return is retired.", file: true, absent: true, flags: "mi", pattern: H("return") + PARA + String.raw`(?:return value|function|statement|keyword)` },
      { name: "no-code-names", why: "No component or function name anywhere in the written glossary. StockLot may be noted as the code's word for batch. Case-sensitive.", file: true, absent: true,
        pattern: String.raw`\b(?:AllocationEngine|PickListBuilder|ReservationService|SkuCache)\b|available_qty|\buow\(` },
      { name: "no-entry-over-80-words", why: "The bloated available entry (130 words) is cut down; the skill's own mark is about fifty.", file: true, absent: true, flags: "m", pattern: OVER_80_WORDS },
      { name: "guidance-cut-from-entry", why: "The sales guidance is not meaning.", file: true, absent: true, flags: "i", pattern: String.raw`call the warehouse` },
      { name: "header-admission-replaced", why: "The header's admission rule ('appears in the code, or a decision introduced it') is replaced by the tests.", file: true, absent: true, flags: "i", pattern: String.raw`appears in the\s+code` },
      { name: "cycle-count-distinction", llm: true, focus: "file",
        criteria: `This is a project glossary. Judge the "cycle count" entry only.

PASS if there is a cycle count entry and it still says how a cycle count differs from a stocktake: it is done while picking carries on, without stopping or closing the warehouse (any wording).
FAIL if there is no cycle count entry, or the entry no longer says how it differs from a stocktake.` },
      // --- the report ---
      { name: "drift-movement-cited", why: "Drift at a known line: MovementKind at stockroom/models.py:38-43 against 'from one bin to another bin'.", pattern: FL("models.py", "3[5-9]|4[0-3]") },
      { name: "edge-contributing-cited", why: "A convention that feeds class names into the glossary: CONTRIBUTING.md:4 (and :8).", pattern: FL("CONTRIBUTING.md", "[3-4]|8") },
      { name: "homeless-sales-guidance", why: "The 'below five, call the warehouse' sentence has no other home and is listed as such.", flags: "i", pattern: near("below five|call the warehouse") },
      { name: "gap-wave-proposed", why: "The gap: wave is used everywhere and never defined. The file has no gaps line, so it is presented in the report.", flags: "i", pattern: String.raw`\bgaps?\b[\s\S]{0,1200}?\bwave\b` },
    ],
  },
  "lexicon-tessera": {
    lexicon: "docs/lexicon.md",
    graders: [
      skillFired,
      { name: "components-retired", why: "Test 1: component names are not entries.", file: true, absent: true, flags: "mi",
        pattern: H("HotkeyListener|LayoutEngine|RuleEngine|WorkspaceManager") },
      { name: "pervasive-identifier-retired", why: "Decoy: ctx is in 8 of 11 source files, and frequency in code is not test 2.", file: true, absent: true, flags: "mi", pattern: H("context") },
      { name: "ordinary-words-retired", why: "Test 2: ordinary words.", file: true, absent: true, flags: "mi", pattern: H("config file|shortcut") },
      { name: "decision-only-retired", why: "The entry only restates ADR 0002's decision; its name is used nowhere else.", file: true, absent: true, flags: "mi", pattern: H("click-to-focus policy") },
      { name: "mechanism-name-retired", why: "Mechanism vs guarantee: the routine's name is not a headword, whether the guarantee is reframed or stays in its existing home.", file: true, absent: true, flags: "mi", pattern: H("orphan sweep") },
      { name: "synonym-merged", why: "Test 3: pane is a synonym of tile and is used nowhere.", file: true, absent: true, flags: "mi", pattern: H("pane") },
      { name: "synonym-recorded-not-used", why: "The merge is recorded in the surviving entry.", file: true, flags: "mi", pattern: H("tile") + PARA + String.raw`\bpane\b` },
      { name: "unused-headword-gone", why: "No source says zoom; the code and every doc say promote.", file: true, absent: true, flags: "mi", pattern: H("zoom") },
      { name: "concept-kept-workspace", guard: true, why: "Decoy: WorkspaceManager and the Workspace class are code, workspace is the concept and stays.", file: true, flags: "mi", pattern: H("workspace") },
      { name: "concept-kept-rule", guard: true, why: "Decoy: the Rule record is a narrow holder; users write rules and say the word.", file: true, flags: "mi", pattern: H("rule") },
      { name: "distinction-move-names-send", why: "The distinction survives and becomes two-sided: the original move entry does not name send.", file: true, flags: "mi", pattern: H("move") + PARA + String.raw`\bsend` },
      { name: "distinction-send-names-move", guard: true, why: "The distinction survives: each entry names the other.", file: true, flags: "mi", pattern: H("send") + PARA + String.raw`\bmove` },
      { name: "redirect-rewritten-unmanaged-window", why: "Decoy: the 'See floating window' stub hides a distinct concept (float vs ignore).", file: true, flags: "mi", pattern: NOT_REDIRECT("unmanaged window") },
      { name: "user-facing-term-kept", guard: true, why: "Decoy: split ratio has a config key but is a word users say and set.", file: true, flags: "mi", pattern: H("split ratio") },
      { name: "domain-term-kept-work-area", guard: true, why: "Owner's ruling: work area is the domain's word with a fixed boundary, not an ordinary word, although the platform uses it too.", file: true, flags: "mi", pattern: H("work area") },
      { name: "no-code-names", why: "No component or identifier anywhere in the written lexicon. Case-sensitive.", file: true, absent: true,
        pattern: String.raw`\b(?:HotkeyListener|LayoutEngine|RuleEngine|WorkspaceManager|WindowMover|WmContext|SecondaryArea|RuleTrigger|RuleAction)\b|\bctx\b` },
      { name: "no-entry-over-80-words", why: "The bloated layout entry (about 160 words) is cut down.", file: true, absent: true, flags: "m", pattern: OVER_80_WORDS },
      { name: "history-cut-from-entry", why: "Why the default layout changed is history, not meaning.", file: true, absent: true, flags: "i", pattern: String.raw`ultrawide|until 0\.4|off-cent` },
      { name: "disputed-universal-not-asserted", why: "Drift: 'applied only once ... ever' is contradicted by RuleTrigger.TitleChange, so the lexicon stops asserting it.", file: true, absent: true, flags: "i", pattern: String.raw`only once|ever triggers a rule again` },
      { name: "header-admission-replaced", why: "The header's admission rule (anything the team has given a name) is replaced.", file: true, absent: true, flags: "i", pattern: String.raw`given something a\s+name` },
      { name: "gap-stack-proposed", why: "The gap: SecondaryArea dodges the undefined domain word stack. The file has a Gaps line, so it goes there: anywhere in the header, above the horizontal rule.", file: true, flags: "mi", pattern: String.raw`^\W{0,3}Gaps\b(?:(?!\n-{3})[\s\S]){0,800}?\bstack\b` },
      // --- the report ---
      { name: "drift-rule-cited", why: "Drift at a known line: enum RuleTrigger at src/Tessera/Rules/Rule.cs:4-11, or its use at RuleEngine.cs:33-37.", pattern: FL("Rule.cs", "[3-9]|1[01]") + "|" + FL("RuleEngine.cs", "3[3-7]") },
      { name: "edge-layout-engine-cited", why: "Outside edge: (lexicon: LayoutEngine) at src/Tessera/Layouts/LayoutEngine.cs:9.", pattern: FL("LayoutEngine.cs", "[7-9]") },
      { name: "edge-wmcontext-cited", why: "Outside edge: (lexicon: context) at src/Tessera/WmContext.cs:39.", pattern: FL("WmContext.cs", "3[7-9]") },
      { name: "edge-configuration-cited", why: "A user reference names the mechanism: docs/configuration.md:105.", pattern: FL("configuration.md", "10[3-5]") },
      { name: "edge-conventions-cited", why: "A convention that feeds class names into the lexicon: docs/conventions.md:8.", pattern: FL("conventions.md", String.raw`8|7\s*[-–]\s*[89]`) },
      { name: "homeless-history-sentence", why: "The columns-until-0.4 sentence has no other home and is listed as such.", flags: "i", pattern: near(String.raw`ultrawide|\b0\.4\b|off-cent|columns until|was columns`) },
      { name: "single-window-sentence-home", llm: true, focus: "last_message",
        criteria: `This is a report on consolidating a project lexicon. Judge one thing only: what it says about the sentence from the old "layout" entry, "When a workspace holds a single window, every layout gives it the whole work area."

The written lexicon is not shown to you, only the report, so silence about this sentence is not a failure.

FAIL if the report lists that sentence, or its substance (a lone window gets the whole work area), among the homeless content or as having no other home.
FAIL if the report names src/Tessera/Workspaces/Workspace.cs as the place where that statement lives.
PASS in every other case: the report names src/Tessera/Layouts/ILayout.cs (a doc comment) as its home, or says the statement stays in the entry, or does not say where it went.` },
    ],
  },
  "lexicon-byre": {
    lexicon: "docs/glossary.md",
    graders: [
      skillFired,
      { name: "components-retired", why: "Test 1: component names are not entries. GroupManager is the component beside the concept management group.", file: true, absent: true, flags: "mi",
        pattern: H("HerdStore|ListBuilder|MeterIngest|GroupManager") },
      { name: "pervasive-identifier-retired", why: "Decoy: Env is in 10 of 11 Go files, and frequency in code is not test 2.", file: true, absent: true, flags: "m", pattern: H("Env") },
      { name: "ordinary-word-retired", why: "Test 2: user, in its ordinary sense. farm is left ungraded: three entries lean on it and the key's builder called keeping it mildly arguable.", file: true, absent: true, flags: "mi", pattern: H("user") },
      { name: "decision-only-retired", why: "The entry only restates decision record 0002; its name is used nowhere else.", file: true, absent: true, flags: "mi", pattern: H("late-reading rule") },
      { name: "mechanism-name-retired", why: "Mechanism vs guarantee: the routine's name is not a headword, whether the guarantee is reframed (withhold list) or stays in its existing home.", file: true, absent: true, flags: "mi", pattern: H("withhold sweep") },
      { name: "synonym-merged", why: "Test 3: lactation number is the same count as parity here, and is used nowhere.", file: true, absent: true, flags: "mi", pattern: H("lactation number") },
      { name: "synonym-recorded-not-used", why: "The merge is recorded in the surviving entry.", file: true, flags: "mi", pattern: H("parity") + PARA + String.raw`lactation number` },
      { name: "unused-headword-gone", why: "No source says days in lactation; the code and every doc say days in milk. True under rename and under retire.", file: true, absent: true, flags: "mi", pattern: H("days in lactation") },
      { name: "concept-kept-management-group", guard: true, why: "Decoy: GroupManager is code, management group is the concept and stays.", file: true, flags: "mi", pattern: H("management group") },
      { name: "sound-term-kept-cow", guard: true, why: "cow has a fixed boundary against heifer: a female that has calved.", file: true, flags: "mi", pattern: H("cow") },
      { name: "distinction-milking-names-session", why: "The distinction survives and becomes two-sided: the original milking entry does not name session.", file: true, flags: "mi", pattern: H("milking") + PARA + String.raw`\bsession` },
      { name: "distinction-session-names-milking", guard: true, why: "The distinction survives. Also the Session struct decoy: a bare key type does not make the word code.", file: true, flags: "mi", pattern: H("session") + PARA + String.raw`\bmilking` },
      { name: "redirect-rewritten-heifer", why: "Decoy: the 'See cow' stub hides a distinct concept the code and docs distinguish everywhere.", file: true, flags: "mi", pattern: NOT_REDIRECT("heifer") },
      { name: "user-facing-term-kept", guard: true, why: "Decoy: VWP has a config key but is a word herd managers say and set. Either form of the headword passes.", file: true, flags: "mi", pattern: String.raw`^\*\*(?:VWP|voluntary waiting period)\b` },
      { name: "no-code-names", why: "No type, routine or identifier anywhere in the written glossary. Case-sensitive.", file: true, absent: true,
        pattern: String.raw`\b(?:HerdStore|ListBuilder|MeterIngest|GroupManager|LactationService|TreatmentService|Insemination|Env)\b|sweepWithheld` },
      { name: "no-entry-over-80-words", why: "The bloated dry period entry (about 155 words) is cut down.", file: true, absent: true, flags: "m", pattern: OVER_80_WORDS },
      { name: "bloated-entry-cut", why: "The history of the default, and the config key, are not meaning.", file: true, absent: true, flags: "i", pattern: String.raw`release 2\.3|dry cow tubes|dry_period_days` },
      { name: "disputed-universal-not-asserted", why: "Drift: 'always withheld from the bulk tank' is false for a meat withdrawal, so the glossary stops asserting it. True whether the entry is rewritten or split in two.", file: true, absent: true, flags: "i", pattern: String.raw`always withheld|never counted as saleable` },
      { name: "header-admission-replaced", why: "The header's admission rule (anything the team has given a name) is replaced.", file: true, absent: true, flags: "i", pattern: String.raw`has given something a\s+name` },
      { name: "gap-service-proposed", why: "The gap: the Insemination type dodges the undefined domain word service. The file has a Gaps line, so it goes there: anywhere in the header, above the horizontal rule.", file: true, flags: "mi", pattern: String.raw`^\W{0,3}Gaps\b(?:(?!\n-{3})[\s\S]){0,800}?\bservice\b` },
      // --- the report ---
      { name: "drift-withdrawal-cited", why: "Drift at a known line: the WithdrawalKind constants at internal/treatment/withdrawal.go:15-20, or their use at :100-102.", pattern: FL("withdrawal.go", "1[3-9]|20|100|101|102") },
      { name: "edge-withdrawal-cited", why: "Outside edge: (glossary: withhold sweep) at internal/treatment/withdrawal.go:90.", pattern: FL("withdrawal.go", "8[89]|9[0-2]") },
      { name: "edge-env-cited", why: "Outside edge: (glossary: Env) at internal/env/env.go:49.", pattern: FL("env.go", "4[7-9]") },
      { name: "edge-configuration-cited", why: "A user reference names the mechanism: docs/configuration.md:29.", pattern: FL("configuration.md", "2[6-9]") },
      { name: "edge-conventions-cited", why: "A convention that feeds type names into the glossary: docs/conventions.md:10-11.", pattern: FL("conventions.md", "1[01]") },
      { name: "homeless-history-sentence", why: "The 56-to-60-days sentence has no other home and is listed as such.", flags: "i", pattern: near(String.raw`release 2\.3|56 days|dry cow tubes|raised to 60`) },
      { name: "forty-day-sentence-home", llm: true, focus: "last_message",
        criteria: `This is a report on consolidating a project glossary. Judge one thing only: what it says about the sentence from the old "dry period" entry, "A cow whose dry period will be shorter than 40 days is marked as short on the calving list."

The written glossary is not shown to you, only the report, so silence about this sentence is not a failure.

FAIL if the report lists that sentence, or its substance (a dry period under 40 days is marked short), among the homeless content or as having no other home.
FAIL if the report names internal/lists/builder.go as the place where that statement lives.
PASS in every other case: the report names internal/lactation/lactation.go (a doc comment) as its home, or says the statement stays in the entry, or does not say where it went.` },
    ],
  },
};

const q = (s) => `'${s.replace(/'/g, "''")}'`;

export function render(c, g) {
  if (g.raw) return `---\n${g.raw}\n---\n`;
  if (g.llm) {
    const focus = g.focus === "file" ? `{ source: file, path: ${c.lexicon} }` : g.focus;
    return `---\ntype: llm\nfocus: ${focus}\n---\n\n${g.criteria}\n`;
  }
  const lines = ["---", `# ${g.why}`, "type: regex"];
  lines.push(g.file ? `target: { source: file, path: ${c.lexicon} }` : "target: last_message");
  lines.push(`pattern: ${q(g.pattern)}`);
  if (g.flags) lines.push(`flags: ${g.flags}`);
  if (g.absent) lines.push("match: not_contains");
  lines.push("---", "");
  return lines.join("\n");
}

if (process.argv[2] === "write") {
  for (const [name, c] of Object.entries(cases)) {
    const dir = `evals/${name}/graders`;
    mkdirSync(dir, { recursive: true });
    let kept = 0;
    for (const g of c.graders) {
      const file = `${dir}/${g.name}.md`;
      if (g.llm && existsSync(file)) { kept++; continue; } // a calibrated rubric, edited by hand
      writeFileSync(file, render(c, g));
    }
    console.log(name, c.graders.length, "graders", kept ? `(${kept} llm rubric left as it is)` : "");
  }
}
