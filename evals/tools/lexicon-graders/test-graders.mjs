// Offline check of the regex graders, at no cost: every pattern must pass a hand-made correct
// output (samples/<fixture>-good-*.md) and fail the untouched fixture with a fooled report.
// A grader marked `guard` protects something the original already has, so it passes both.
// Run from the repository root, before spending a run on a changed pattern.
import { readFileSync } from "node:fs";
import { cases } from "./gen-graders.mjs";

const S = new URL("./samples/", import.meta.url).pathname;
const inputs = {
  "lexicon-shelfwise": {
    good: { file: S + "shelfwise-good-lexicon.md", msg: S + "shelfwise-good-report.md" },
    bad: { file: "evals/lexicon-shelfwise/fixture/docs/design/lexicon.md", msg: S + "shelfwise-fooled-report.md" },
  },
  "lexicon-stockroom": {
    good: { file: S + "stockroom-good-lexicon.md", msg: S + "stockroom-good-report.md" },
    bad: { file: "evals/lexicon-stockroom/fixture/GLOSSARY.md", msg: S + "shelfwise-fooled-report.md" },
  },
  "lexicon-tessera": {
    good: { file: S + "tessera-good-lexicon.md", msg: S + "tessera-good-report.md" },
    bad: { file: "evals/lexicon-tessera/fixture/docs/lexicon.md", msg: S + "shelfwise-fooled-report.md" },
  },
  "lexicon-byre": {
    good: { file: S + "byre-good-lexicon.md", msg: S + "byre-good-report.md" },
    bad: { file: "evals/lexicon-byre/fixture/docs/glossary.md", msg: S + "shelfwise-fooled-report.md" },
  },
};
const verdict = (g, text) => {
  const found = new RegExp(g.pattern, g.flags ?? "").test(text);
  return g.absent ? !found : found;
};

let problems = 0;
for (const [name, c] of Object.entries(cases)) {
  for (const g of c.graders) {
    if (g.raw || g.llm) continue;
    const r = {};
    for (const side of ["good", "bad"]) {
      const text = readFileSync(g.file ? inputs[name][side].file : inputs[name][side].msg, "utf8");
      r[side] = verdict(g, text);
    }
    const ok = r.good && (g.guard ? r.bad : !r.bad); // a guard protects what the original already has
    if (!ok) problems++;
    console.log(`${ok ? "ok  " : "LOOK"} ${name}/${g.name}  good=${r.good} bad=${r.bad}`);
  }
}
console.log(problems ? `${problems} to look at` : "all regex graders separate good from bad");
